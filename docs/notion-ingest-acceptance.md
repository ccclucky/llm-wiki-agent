# Notion-first Ingest acceptance

This checklist verifies a real Agent's Skill + Notion MCP integration. It is intentionally independent of any one Notion account: discover page IDs and data-source URLs from the connected workspace at runtime.

## Safety and preflight

- Use a real, non-sensitive source that the user wants to preserve. Do not create throwaway personal-knowledge records merely to test the integration.
- Confirm the Agent is connected to the intended CCLUCKY Knowledge OS workspace.
- Read the root page, Agent Context Protocol, and current Inbox data-source schema.
- Confirm access to Inbox, Sources, Entities, Concepts, Syntheses, and System as needed.
- Check whether the source already exists by URL, title, or stable fingerprint.
- Never put workspace-specific page IDs, private source contents, or credentials into this public repository.

## End-to-end test

1. **Capture:** create a Inbox record with Status = Inbox, accurate Source Type, source date/origin, Captured By, useful Tags, and original content in the page body.
2. **Claim:** re-fetch the record; if another active Agent has claimed it, stop. Set Status = Processing, Processing By, and Processing Started At.
3. **Resolve:** search for existing canonical pages before creating anything. Distinguish source facts, user statements, source claims, analysis, and hypotheses.
4. **Write:** create/update one Source page and only the necessary Entity / Concept pages. Preserve source provenance and dates.
5. **Link:** create Notion-native page mentions to exact page URLs returned by Notion. A plain URL or title is not enough.
6. **Verify:** query backlinks on the target pages and confirm the expected inbound references exist. Add a meaningful link from the Inbox record to its resulting Source page so the intake item can be traced to its output.
7. **Complete:** only after the checks pass, set Status = Processed, populate Processed At and Ingest Summary, and preserve the Inbox record.
8. **Recover:** if the result cannot be safely completed, use Needs Review and record partial progress / the blocker in Processing Notes. Never mark a partial ingest Processed.

## Multi-agent concurrency

Processing By and Processing Started At are advisory coordination fields, not an atomic distributed lock. Agents must re-fetch before claiming, avoid simultaneous edits to the same Inbox record, and inspect partial writes before reclaiming a stale Processing record. Do not claim that this design guarantees exactly-once processing.

## Cross-agent acceptance matrix

Run this independently in every target client. A successful ChatGPT connection does not prove another client's MCP access or Skill loading.

| Client | Skill loads | Notion search/read | Inbox create/update | Native mention | Backlink query | Result |
|---|---|---|---|---|---|---|
| Claude Code | Pending | Pending | Pending | Pending | Pending | Pending |
| Codex | Pending | Pending | Pending | Pending | Pending | Pending |
| WorkBuddy | Pending | Pending | Pending | Pending | Pending | Pending |

Record capability gaps per client. If a client cannot create native mentions or inspect backlinks, report the limitation instead of silently replacing them with ordinary links.
