# Query and update workflows

## Query

When the user asks what the wiki knows about a subject:

1. Search the canonical Notion workspace for the main subject and relevant aliases.
2. Read the matching Entity or Concept page, not just the search snippet.
3. Follow native mentions and backlinks to relevant Sources, Projects, Concepts, and Syntheses.
4. Read enough source pages to support the answer. Prefer primary evidence and recent updates; do not assume the most recently edited page is the most authoritative.
5. Separate verified facts, user-reported statements, source claims, analysis, and hypotheses.
6. Answer with Notion page links/citations where the client supports them. Cite the underlying source page, not only a synthesis.
7. Save a new Synthesis only when the user asks, or when the user explicitly asks to preserve the answer as knowledge.

Do not query only RAW by default. RAW is the intake archive; the processed wiki pages are the knowledge layer.

## Update an existing page

When the user supplies new information about an existing project, person, concept, or decision:

1. Search for the canonical page.
2. Fetch the page and inspect its current content before editing.
3. Determine whether the new information adds a fact, changes a status, supersedes an old decision, or conflicts with existing evidence.
4. Preserve the previous state when it is historically meaningful. Add dates and mark superseded information instead of silently rewriting history.
5. Add provenance: link the relevant RAW source or other source page using a native Notion mention.
6. Update related Entity / Concept / Synthesis pages only when the new information materially affects them.
7. Verify the edit and important backlinks.

Prefer a targeted update. Do not replace an entire page if a small append or targeted edit is sufficient.

## Conflict handling

If two sources disagree:
- preserve both claims and their source/date;
- state exactly what conflicts;
- assess source authority and recency without assuming the newer source is always correct;
- mark the issue as unresolved or Needs Review when necessary;
- do not choose a winner without adequate evidence.

## Personal and sensitive information

Only preserve sensitive or highly personal information when it is clearly relevant to the user's requested long-term knowledge purpose. Never store credentials, access tokens, passwords, private keys, session cookies, or security answers. See [security-and-concurrency.md](security-and-concurrency.md).