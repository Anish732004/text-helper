# Text Helper — Streamlit App

A small Streamlit app that lets a user upload a `.txt` file, preview the content, apply string operations, and (in Append mode) save the edited file.

## Files
- `app.py` — main Streamlit app
- `text_utils.py` — pure helper functions for string operations
- `requirements.txt` — Python dependencies
- `.streamlit/config.toml` — optional Streamlit config
- `README.md` — this file

## How to run locally
1. Create a virtual environment and activate it.
2. `pip install -r requirements.txt`
3. `streamlit run app.py`

## Deploying to Streamlit Cloud
1. Push this repository to GitHub.
2. On Streamlit Cloud (https://streamlit.io/cloud), connect your GitHub repo and deploy.
3. Streamlit will install dependencies from `requirements.txt` and run `app.py`.

## Acceptance checklist (implemented)
- Upload rejects non-.txt files (UI & explicit suffix check).
- Preview shows first 20 lines and stats (lines, words, characters).
- Buttons perform string operations and update preview.
- Append mode enables adding extra text and downloading edited file.
- Read mode disables saving with a clear message.
- Timestamp is added on save.
- Helper functions are pure and located in `text_utils.py`.
