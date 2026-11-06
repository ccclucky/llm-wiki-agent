# Knowledge update workflow

Use this workflow when the user asks to update, correct, supersede, or reconcile existing knowledge.

## Update

1. Search for the canonical page and fetch its current content before editing.
2. Determine whether the new information adds a fact, changes a status, supersedes a decision, or conflicts with existing evidence.
3. Preserve previous state when historically meaningful. Add dates and mark superseded information instead of silently rewriting history.
4. Add provenance using a native Notion mention to the supporting Rows record or Source page.
5. Update related Entity, Concept, or Synthesis pages only when materially affected.
6. Prefer targeted edits. Re-fetch after writing and verify important links.
7. If the page cannot be found, search aliases and related pages before proposing a new canonical page.

## Conflicts

If two sources disagree:
- preserve both claims and their source/date;
- state exactly what conflicts;
- assess source authority and recency without assuming newer always means correct;
- mark unresolved items for review;
- do not choose a winner without adequate evidence.

## Personal and sensitive information

Only preserve sensitive or highly personal information when clearly relevant to the user's requested long-term knowledge purpose. Never store credentials, access tokens, passwords, private keys, session cookies, or security answers.

## Safety

Do not delete, merge, or broadly restructure pages unless the user explicitly approves the exact change. Never overwrite another agent's newer edits. Fetch before editing and re-fetch before retrying a timed-out write.
