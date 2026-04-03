# Decisions

## D-001: Git tags are the rollback anchor

- Date: 2026-04-03
- Decision: Every meaningful portfolio checkpoint gets an annotated git tag such as `v0.3.0`.
- Why: A named tag is easier to restore than remembering raw commit hashes.

## D-002: Tagged versions need a visual snapshot

- Date: 2026-04-03
- Decision: Every tagged version keeps a desktop full-page screenshot in `docs/versions/assets/`.
- Why: The portfolio is visual work, so the written changelog alone is not enough.

## D-003: Commits stay segmented by concern

- Date: 2026-04-03
- Decision: Documentation/process changes, visible site changes, and archival snapshot updates should be committed separately whenever practical.
- Why: Clean history makes it easier to review, revert, and explain changes later.

## D-004: Current-site rollback matters more than perfect release automation

- Date: 2026-04-03
- Decision: Use lightweight local scripts and repo docs instead of a heavy release system.
- Why: The project is a single Streamlit portfolio, so a simple workflow is easier to keep up to date.
