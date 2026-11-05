#!/usr/bin/env python3
"""Publish the local Markdown wiki to a Notion workspace.

The first integration milestone is intentionally one-way: Git/Markdown remains
the canonical source, while Notion is a browsable mirror. Only blocks created
by this tool are replaced on subsequent syncs; manually added blocks are kept.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
WIKI_DIR = REPO_ROOT / "wiki"
STATE_FILE = REPO_ROOT / ".notion-sync-state.json"
NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*(?:\n|$)", re.DOTALL)
TITLE_RE = re.compile(r"^title:\s*(.*?)\s*$", re.MULTILINE)
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]|\[([^\]]+)\]\((https?://[^)\s]+)\)")
HEADING_RE = re.compile(r"^(#{1,3})\s+(.+?)\s*$")
BULLET_RE = re.compile(r"^\s*[-*+]\s+(.+)$")
NUMBER_RE = re.compile(r"^\s*\d+[.)]\s+(.+)$")
QUOTE_RE = re.compile(r"^\s*>\s?(.*)$")
FENCE_RE = re.compile(r"^\s*" + re.escape(chr(96) * 3) + r"([A-Za-z0-9_+-]*)\s*$")

CATEGORY_NAMES = {
    "sources": "Sources",
    "entities": "Entities",
    "concepts": "Concepts",
    "syntheses": "Syntheses",
}
SYSTEM_FILES = {"index.md", "overview.md", "log.md", "lint-report.md"}
CODE_LANGUAGES = {
    "bash", "c", "clojure", "coffeescript", "cpp", "csharp", "css", "dart",
    "diff", "docker", "elixir", "elm", "erlang", "flow", "fortran", "fsharp",
    "gherkin", "glsl", "go", "graphql", "groovy", "haskell", "html", "java",
    "javascript", "json", "julia", "kotlin", "latex", "less", "lisp", "lua",
    "makefile", "markdown", "matlab", "mermaid", "nix", "objective-c", "ocaml",
    "pascal", "perl", "php", "plain text", "powershell", "prolog", "protobuf",
    "python", "r", "reason", "ruby", "rust", "sass", "scala", "scheme", "scss",
    "shell", "sql", "swift", "typescript", "vb.net", "verilog", "vhdl", "xml",
    "yaml",
}


class NotionAPIError(RuntimeError):
    def __init__(self, status: int, message: str):
        super().__init__(f"Notion API returned HTTP {status}: {message}")
        self.status = status


class NotionClient:
    """Small standard-library Notion API client; no extra dependency required."""

    def __init__(self, token: str, timeout: int = 30):
        self.token = token
        self.timeout = timeout

    def request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        url = NOTION_API_BASE + path
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        }
        request = urllib.request.Request(url, data=data, headers=headers, method=method)

        for attempt in range(4):
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    body = response.read()
                    return json.loads(body.decode("utf-8")) if body else {}
            except urllib.error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                try:
                    detail = json.loads(body)
                    message = detail.get("message") or detail.get("code") or body
                except json.JSONDecodeError:
                    message = body
                if exc.code in (429, 500, 502, 503, 504) and attempt < 3:
                    retry_after = exc.headers.get("Retry-After")
                    try:
                        delay = float(retry_after) if retry_after else min(2 ** attempt, 8)
                    except ValueError:
                        delay = min(2 ** attempt, 8)
                    time.sleep(min(delay, 30))
                    continue
                raise NotionAPIError(exc.code, str(message)[:500]) from None
            except urllib.error.URLError as exc:
                if attempt < 3:
                    time.sleep(min(2 ** attempt, 8))
                    continue
                raise RuntimeError(f"Could not reach Notion API: {exc.reason}") from None

        raise RuntimeError("Notion API request failed after retries")

    def create_page(self, parent_page_id: str, title: str) -> dict[str, Any]:
        return self.request("POST", "/pages", {
            "parent": {"type": "page_id", "page_id": parent_page_id},
            "properties": {"title": {"title": [{"type": "text", "text": {"content": title[:2000]}}]}},
        })

    def update_page_title(self, page_id: str, title: str) -> None:
        self.request("PATCH", f"/pages/{page_id}", {
            "properties": {"title": {"title": [{"type": "text", "text": {"content": title[:2000]}}]}},
        })

    def list_child_pages(self, block_id: str) -> dict[str, str]:
        """Return immediate child pages keyed by title, following Notion pagination."""
        pages: dict[str, str] = {}
        cursor: str | None = None
        while True:
            query = {"page_size": 100}
            if cursor:
                query["start_cursor"] = cursor
            path = f"/blocks/{block_id}/children?{urllib.parse.urlencode(query)}"
            result = self.request("GET", path)
            for block in result.get("results", []):
                if block.get("type") == "child_page":
                    title = block.get("child_page", {}).get("title", "")
                    if title and block.get("id"):
                        pages.setdefault(title, block["id"])
            if not result.get("has_more"):
                break
            cursor = result.get("next_cursor")
            if not cursor:
                break
        return pages

    def append_children(self, block_id: str, children: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not children:
            return []
        result = self.request("PATCH", f"/blocks/{block_id}/children", {"children": children})
        return result.get("results", [])

    def delete_block(self, block_id: str) -> None:
        try:
            self.request("DELETE", f"/blocks/{block_id}")
        except NotionAPIError as exc:
            if exc.status != 404:
                raise


def strip_frontmatter(markdown: str) -> str:
    return FRONTMATTER_RE.sub("", markdown, count=1).strip()


def page_title(relative_path: str, markdown: str) -> str:
    match = TITLE_RE.search(markdown)
    if match:
        value = match.group(1).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        if value:
            return value[:2000]
    return Path(relative_path).stem.replace("-", " ").replace("_", " ").title()


def section_for(relative_path: str) -> str:
    path = Path(relative_path)
    if len(path.parts) > 1 and path.parts[0] in CATEGORY_NAMES:
        return CATEGORY_NAMES[path.parts[0]]
    if path.name in SYSTEM_FILES:
        return "System"
    return "Other"


def _append_text_runs(runs: list[dict[str, Any]], text: str, url: str | None = None) -> None:
    for offset in range(0, len(text), 2000):
        chunk = text[offset:offset + 2000]
        if not chunk:
            continue
        text_value: dict[str, Any] = {"content": chunk}
        if url:
            text_value["link"] = {"url": url}
        runs.append({"type": "text", "text": text_value})


def rich_text_runs(text: str, page_lookup: dict[str, str] | None = None) -> list[dict[str, Any]]:
    """Convert Markdown links and [[wikilinks]] into Notion rich-text links."""
    page_lookup = page_lookup or {}
    runs: list[dict[str, Any]] = []
    cursor = 0
    for match in LINK_RE.finditer(text):
        if match.start() > cursor:
            _append_text_runs(runs, text[cursor:match.start()])
        wiki_target = match.group(1)
        if wiki_target is not None:
            label = wiki_target.strip()
            page_id = page_lookup.get(label.casefold())
            if page_id:
                _append_text_runs(runs, label, f"https://www.notion.so/{page_id.replace('-', '')}")
            else:
                _append_text_runs(runs, f"[[{label}]]")
        else:
            _append_text_runs(runs, match.group(2), match.group(3))
        cursor = match.end()
    if cursor < len(text):
        _append_text_runs(runs, text[cursor:])
    return runs


def _text_blocks(
    block_type: str,
    text: str,
    page_lookup: dict[str, str],
    extra: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    runs = rich_text_runs(text, page_lookup)
    blocks = []
    for offset in range(0, len(runs), 100):
        body = dict(extra or {})
        body["rich_text"] = runs[offset:offset + 100]
        blocks.append({"object": "block", "type": block_type, block_type: body})
    return blocks


def markdown_to_blocks(markdown: str, page_lookup: dict[str, str] | None = None) -> list[dict[str, Any]]:
    """Convert common Markdown structures into Notion block payloads."""
    page_lookup = page_lookup or {}
    lines = strip_frontmatter(markdown).splitlines()
    blocks: list[dict[str, Any]] = []
    paragraph: list[str] = []
    quote: list[str] = []
    code: list[str] = []
    in_code = False
    code_language = "plain text"

    def flush_paragraph() -> None:
        if paragraph:
            blocks.extend(_text_blocks("paragraph", "\n".join(paragraph), page_lookup))
            paragraph.clear()

    def flush_quote() -> None:
        if quote:
            blocks.extend(_text_blocks("quote", "\n".join(quote), page_lookup))
            quote.clear()

    def flush_code() -> None:
        if code:
            language = code_language if code_language in CODE_LANGUAGES else "plain text"
            blocks.extend(_text_blocks("code", "\n".join(code), {}, {"language": language}))
            code.clear()

    for line in lines:
        fence = FENCE_RE.match(line)
        if in_code:
            if fence:
                flush_code()
                in_code = False
            else:
                code.append(line)
            continue
        if fence:
            flush_paragraph()
            flush_quote()
            in_code = True
            code_language = (fence.group(1) or "plain text").lower()
            continue

        heading = HEADING_RE.match(line)
        bullet = BULLET_RE.match(line)
        number = NUMBER_RE.match(line)
        quoted = QUOTE_RE.match(line)

        if not line.strip():
            flush_paragraph()
            flush_quote()
        elif re.match(r"^(?:---|\*\*\*|___)\s*$", line.strip()):
            flush_paragraph()
            flush_quote()
            blocks.append({"object": "block", "type": "divider", "divider": {}})
        elif heading:
            flush_paragraph()
            flush_quote()
            level = len(heading.group(1))
            blocks.extend(_text_blocks(f"heading_{level}", heading.group(2), page_lookup))
        elif bullet:
            flush_paragraph()
            flush_quote()
            blocks.extend(_text_blocks("bulleted_list_item", bullet.group(1), page_lookup))
        elif number:
            flush_paragraph()
            flush_quote()
            blocks.extend(_text_blocks("numbered_list_item", number.group(1), page_lookup))
        elif quoted:
            flush_paragraph()
            quote.append(quoted.group(1))
        else:
            flush_quote()
            paragraph.append(line)

    if in_code:
        flush_code()
    flush_paragraph()
    flush_quote()
    return blocks


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"version": 1, "root_page_id": None, "containers": {}, "pages": {}}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Sync state is not valid JSON: {path}. Inspect it before changing it.") from exc
    if state.get("version") != 1:
        raise RuntimeError(f"Unsupported Notion sync state version: {state.get('version')}")
    state.setdefault("containers", {})
    state.setdefault("pages", {})
    return state


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def _wiki_files(wiki_dir: Path) -> list[Path]:
    return sorted(path for path in wiki_dir.rglob("*.md") if path.is_file())


def _ensure_container(
    client: NotionClient,
    root_page_id: str,
    category: str,
    state: dict[str, Any],
    state_path: Path,
) -> str:
    page_id = state["containers"].get(category)
    if page_id:
        return page_id

    # Reuse pages the user already created in Notion. This is important when
    # bootstrapping an existing workspace: never create duplicate category
    # pages simply because the local sync-state file does not exist yet.
    existing_pages = client.list_child_pages(root_page_id)
    page_id = existing_pages.get(category)
    if not page_id:
        created = client.create_page(root_page_id, category)
        page_id = created["id"]

    state["containers"][category] = page_id
    save_state(state_path, state)
    return page_id


def _delete_tracked_blocks(client: NotionClient, block_ids: list[str]) -> None:
    for block_id in block_ids:
        client.delete_block(block_id)


def _sync_page_content(
    client: NotionClient,
    page_id: str,
    markdown: str,
    page_lookup: dict[str, str],
    entry: dict[str, Any],
    state: dict[str, Any],
    state_path: Path,
) -> None:
    pending = entry.get("pending_block_ids", [])
    if pending:
        _delete_tracked_blocks(client, pending)
        entry["pending_block_ids"] = []
        save_state(state_path, state)

    old_block_ids = list(entry.get("block_ids", []))
    blocks = markdown_to_blocks(markdown, page_lookup)
    new_block_ids: list[str] = []

    for offset in range(0, len(blocks), 100):
        created = client.append_children(page_id, blocks[offset:offset + 100])
        new_block_ids.extend(item["id"] for item in created if item.get("id"))
        entry["pending_block_ids"] = list(new_block_ids)
        save_state(state_path, state)

    _delete_tracked_blocks(client, old_block_ids)
    entry["block_ids"] = new_block_ids
    entry["pending_block_ids"] = []
    entry["content_hash"] = hashlib.sha256(markdown.encode("utf-8")).hexdigest()
    entry["last_synced_at"] = datetime.now(timezone.utc).isoformat()
    save_state(state_path, state)


def sync(
    wiki_dir: Path,
    state_path: Path,
    root_page_id: str,
    client: NotionClient,
    force: bool = False,
    limit: int | None = None,
) -> dict[str, int]:
    if not wiki_dir.exists():
        raise RuntimeError(f"Wiki directory does not exist: {wiki_dir}")

    state = load_state(state_path)
    previous_root = state.get("root_page_id")
    if previous_root and previous_root != root_page_id:
        raise RuntimeError(
            "NOTION_PARENT_PAGE_ID differs from the root page recorded in the sync state. "
            "Use a separate state file for each Notion workspace."
        )
    state["root_page_id"] = root_page_id
    files = _wiki_files(wiki_dir)
    if limit is not None:
        files = files[:limit]
    if not files:
        print("No Markdown pages found.")
        return {"created": 0, "updated": 0, "unchanged": 0}

    categories = sorted({section_for(path.relative_to(wiki_dir).as_posix()) for path in files})
    container_ids = {
        category: _ensure_container(client, root_page_id, category, state, state_path)
        for category in categories
    }

    changed: list[tuple[Path, str, str, dict[str, Any]]] = []
    newly_created: set[str] = set()
    created_count = 0
    unchanged_count = 0

    for path in files:
        relative = path.relative_to(wiki_dir).as_posix()
        markdown = path.read_text(encoding="utf-8")
        title = page_title(relative, markdown)
        entry = state["pages"].get(relative)
        if entry is None:
            remote = client.create_page(container_ids[section_for(relative)], title)
            entry = {
                "id": remote["id"],
                "title": title,
                "content_hash": "",
                "block_ids": [],
                "pending_block_ids": [],
            }
            state["pages"][relative] = entry
            newly_created.add(relative)
            save_state(state_path, state)
            created_count += 1
        elif entry.get("title") != title:
            client.update_page_title(entry["id"], title)
            entry["title"] = title
            save_state(state_path, state)

        digest = hashlib.sha256(markdown.encode("utf-8")).hexdigest()
        if force or digest != entry.get("content_hash") or entry.get("pending_block_ids"):
            changed.append((path, relative, markdown, entry))
        else:
            unchanged_count += 1

    page_lookup: dict[str, str] = {}
    for relative, entry in state["pages"].items():
        title = entry.get("title", "")
        if title:
            page_lookup[title.casefold()] = entry["id"]
        page_lookup[Path(relative).stem.casefold()] = entry["id"]

    updated_count = 0
    for _path, relative, markdown, entry in changed:
        _sync_page_content(client, entry["id"], markdown, page_lookup, entry, state, state_path)
        if relative not in newly_created:
            updated_count += 1
        print(f"  synced: {relative}")

    return {"created": created_count, "updated": updated_count, "unchanged": unchanged_count}


def dry_run(wiki_dir: Path, state_path: Path, limit: int | None = None) -> dict[str, int]:
    state = load_state(state_path)
    files = _wiki_files(wiki_dir)
    if limit is not None:
        files = files[:limit]
    counts = {"new": 0, "changed": 0, "unchanged": 0}
    for path in files:
        relative = path.relative_to(wiki_dir).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        entry = state["pages"].get(relative)
        if entry is None:
            counts["new"] += 1
        elif digest != entry.get("content_hash"):
            counts["changed"] += 1
        else:
            counts["unchanged"] += 1
    print("Dry run only — no Notion API calls will be made.")
    print(f"Pages: {len(files)} | New: {counts['new']} | Changed: {counts['changed']} | Unchanged: {counts['unchanged']}")
    print("This preview uses local sync state and does not verify remote Notion pages.")
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish the local LLM Wiki to Notion.")
    parser.add_argument("--dry-run", action="store_true", help="Preview local changes without calling Notion.")
    parser.add_argument("--force", action="store_true", help="Re-publish every page, even if its hash is unchanged.")
    parser.add_argument("--limit", type=int, help="Limit the number of Markdown pages (useful for first-time testing).")
    parser.add_argument("--wiki-dir", type=Path, default=WIKI_DIR, help="Path to the local wiki directory.")
    parser.add_argument("--state-file", type=Path, default=STATE_FILE, help="Path to the local sync state file.")
    args = parser.parse_args()

    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be at least 1")
    if args.dry_run:
        dry_run(args.wiki_dir, args.state_file, args.limit)
        return 0

    token = os.getenv("NOTION_API_KEY")
    root_page_id = os.getenv("NOTION_PARENT_PAGE_ID")
    if not token or not root_page_id:
        print(
            "Missing Notion configuration. Set NOTION_API_KEY and NOTION_PARENT_PAGE_ID; "
            "see docs/notion-setup.md.",
            file=sys.stderr,
        )
        return 2

    client = NotionClient(token)
    try:
        result = sync(args.wiki_dir, args.state_file, root_page_id, client, force=args.force, limit=args.limit)
    except (NotionAPIError, RuntimeError, OSError, KeyError) as exc:
        print(f"Notion sync failed: {exc}", file=sys.stderr)
        return 1

    print(
        "Notion sync complete — "
        f"created: {result['created']}, updated: {result['updated']}, "
        f"unchanged: {result['unchanged']}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
