# Text Helper — Streamlit App (Kindle-style reader)

Features
- Accepts `.txt` (full features) and `.pdf` (read-only) uploads.
- Kindle-style reader for both `.txt` and `.pdf` in Read mode:
  - Sepia background, serif font, comfortable line spacing, centered column.
- PDF page navigation (Prev / Next).
- Append mode (for `.txt` only) with string tools:
  - UPPERCASE, lowercase, strip, Capitalize, Title Case
  - Replace, Count substring, Append extra text and download edited file.
- String helper functions are in `text_utils.py`.

How to run locally
1. Create a virtual environment and activate it.
2. `pip install -r requirements.txt`
3. `streamlit run app.py`

Deploying to Streamlit Cloud
1. Push this repository to GitHub.
2. On Streamlit Cloud, connect the GitHub repo and deploy.
3. Streamlit will install dependencies from `requirements.txt` and run `app.py`.
