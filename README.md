# Tim Heid Portfolio

Interactive Streamlit portfolio based on the Babelsberg application PDF, with directly playable project videos.

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
- Contact placeholders still need final values for email / Instagram / website.

## Public deployment

For a stable public URL, push this repo to GitHub and deploy `app.py` on Streamlit Community Cloud.
