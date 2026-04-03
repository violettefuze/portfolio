# Tim Heid Portfolio

Interactive Streamlit portfolio based on the Babelsberg application PDF, with directly playable project videos and a more editorial, production-site inspired layout.

## Local run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py
```

## Project structure

- `app.py` - Streamlit app
- `data/portfolio_content.json` - editable portfolio data
- `assets/images/` - stills extracted from the PDF
- `Bewerbung_Tim_Heid_Babelsberg.pdf` - original source PDF

## Notes

- The PDF text and stills were extracted successfully.
- The PDF itself contains no embedded clickable URLs, so video links were taken from the conversation context and can be updated in `data/portfolio_content.json`.
- Contact data currently uses the values from the business card files. Instagram can still be added later.
- The current structure takes inspiration from production-company websites like FrameArt without copying their wording.

## Public deployment

For a stable public URL, push this repo to GitHub and deploy `app.py` on Streamlit Community Cloud.

## Versioning

The repo now keeps a lightweight history system:

- `CHANGELOG.md` records version summaries.
- `docs/DECISIONS.md` stores durable workflow decisions.
- `docs/NOTES.md` stores the day-to-day operating rules.
- `docs/versions/` stores per-version notes and site snapshots.

To capture a new homepage snapshot locally:

```bash
.venv/bin/pip install -r requirements-tools.txt
.venv/bin/playwright install chromium
.venv/bin/python scripts/capture_site_snapshot.py --output docs/versions/assets/manual-check.png
```
