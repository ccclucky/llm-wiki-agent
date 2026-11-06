# Notion-first Skill suite acceptance

This checklist verifies the complete CCLUCKY Knowledge Skills suite together with a real Notion MCP connection. Skill installation and Notion access are separate concerns; verify both in every target client.

## Skill installation preflight

Confirm the client can discover these eight Skills:

- `kb`
- `kb-setup`
- `kb-ingest`
- `kb-query`
- `kb-update`
- `kb-lint`
- `kb-graph`
- `knowledge-context`

Verify that `/kb` lists the command set, `/kb-setup` is explicitly user-invoked, and the five workflow Skills can be invoked by command/name. Confirm `knowledge-context` is available for automatic invocation and can be called by workflow Skills.

## Safety and workspace preflight

- Use the intended CCLUCKY Knowledge OS workspace.
- Run `/kb-setup` and inspect its read-only readiness report.
- Read the root page, Agent Context Protocol/current System guidance, and live Rows data-source schema.
- Confirm access to Inbox, Rows, Sources, Entities, Concepts, Syntheses, and System as needed.
- Use a real, non-sensitive source the user wants to preserve, or a test source explicitly approved by the user.
- Check whether the source already exists by URL, title, or stable fingerprint.
- Never put workspace-specific page IDs, private source content, or credentials into this public repository.

## End-to-end ingest test

1. **Capture:** invoke `/kb-ingest` with the approved source. Create a Rows record with Status = Pending, accurate Source Type, source date/origin, Captured By, useful Tags, and original content in the page body.
2. **Claim:** re-fetch the record; if another active Agent has claimed it, stop. Set Status = Processing, Processing By, and Processing Started At.
3. **Resolve:** search for existing canonical pages before creating anything. Distinguish source facts, user statements, source claims, analysis, and hypotheses.
4. **Write:** create/update one Source page and only necessary Entity / Concept pages. Preserve source provenance and dates.
5. **Link:** create Notion-native page mentions to exact page URLs returned by Notion. A plain URL or title is not enough.
6. **Verify:** query backlinks on target pages and confirm expected inbound references exist. Add a meaningful link from the Rows record to its resulting Source page so the intake item can be traced to its output.
7. **Complete:** only after checks pass, set Status = Processed, populate Processed At and Ingest Summary, and preserve the Rows record.
8. **Recover:** if the result cannot be safely completed, use Needs Review and record partial progress / blocker in Processing Notes. Never mark a partial ingest Processed.

## Other command checks

- `/kb-query`: answer a question using canonical pages and underlying source evidence; do not create a Synthesis unless asked.
- `/kb-update`: update a test-approved existing page with targeted edits, provenance, and history preserved.
- `/kb-lint`: produce a bounded, read-only quality report with evidence and severity.
- `/kb-graph`: map actual native mentions/backlinks and label inferred edges; state coverage limitations.
- `/kb`: route to the correct workflow without performing an unrequested write.

## Multi-agent concurrency

Processing By and Processing Started At are advisory coordination fields, not an atomic distributed lock. Agents must re-fetch before claiming, avoid simultaneous edits to the same Rows record, and inspect partial writes before reclaiming a stale Processing record. Do not claim this design guarantees exactly-once processing.

## Cross-agent acceptance matrix

Run this independently in every target client. A successful ChatGPT connection does not prove another client's MCP access or Skill loading.

| Client | All 8 Skills load | Notion search/read | Rows create/update | Native mention | Backlink query | Result |
|---|---|---|---|---|---|---|
| Claude Code | Pending | Pending | Pending | Pending | Pending | Pending |
| Codex | Pending | Pending | Pending | Pending | Pending | Pending |
| WorkBuddy | Pending | Pending | Pending | Pending | Pending | Pending |

Record capability gaps per client. If a client cannot create native mentions or inspect backlinks, report the limitation instead of silently replacing them with ordinary links.
