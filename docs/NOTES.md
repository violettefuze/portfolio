# Notes

## Working Rules

- Check `CHANGELOG.md`, `docs/DECISIONS.md`, and recent commits before making a new round of changes.
- Keep commits segmented by concern whenever possible.
- Cut a new version only when the site reaches a coherent checkpoint that we may want to revisit later.
- For each tagged version, save a homepage snapshot to `docs/versions/assets/` and add or update a matching note in `docs/versions/`.
- Use tags, not memory, as the main way to return to an older version.
- If a change only affects process docs or tooling and does not change the visible portfolio, it does not need its own site version tag.

## Rollback Shortcuts

- Review a version without changing branches: `git switch --detach v0.2.0`
- Return to the latest main branch state: `git switch main`
- Compare two versions quickly: `git diff v0.2.0..v0.3.0`

## Snapshot Rules

- Capture the local Streamlit homepage at desktop width.
- Use a full-page screenshot so the archive shows more than just the hero section.
- Store snapshots with the version name in the filename.

## Repo Notes

- The portfolio app lives in `app.py`.
- Editable content lives in `data/portfolio_content.json`.
- Business card PDFs, logo files, and pictogram files are kept as source references for branding and contact details.
