import streamlit as st
from pathlib import Path
from datetime import datetime
import text_utils
try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None

st.set_page_config(page_title="Text Helper (Kindle-style)", layout="centered")

# Simple Kindle-style CSS
READER_CSS = '''
<style>
.reader {
    background: #f4ecd8;
    padding: 36px 48px;
    border-radius: 12px;
    max-width: 700px;
    margin: 24px auto;
    font-family: Georgia, "Times New Roman", Times, serif;
    line-height: 1.6;
    font-size: 18px;
    color: #2b2b2b;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}
.reader p { margin: 0 0 1em 0; }
.reader .meta { font-size: 13px; color: #5b5b5b; margin-bottom: 12px; }
.reader .page-nav { display:flex; justify-content:space-between; margin-top:12px; }
.controls { display:flex; gap:8px; align-items:center; }
</style>
'''

st.markdown("# Text Helper — Kindle-style Reader")
uploaded = st.file_uploader("Upload a .txt or .pdf file", type=["txt","pdf"])

if not uploaded:
    st.info("Please upload a .txt or .pdf file to begin.")
    st.stop()

suffix = Path(uploaded.name).suffix.lower()
is_pdf = suffix == ".pdf"
is_txt = suffix == ".txt"

# Read bytes
raw = uploaded.getvalue()

# Extract text
pdf_page_count = 0
pdf_pages_text = []

if is_pdf:
    if fitz is None:
        st.error("PDF support requires PyMuPDF (fitz). Make sure PyMuPDF is installed.")
        st.stop()
    try:
        pdf_doc = fitz.open(stream=raw, filetype="pdf")
        pdf_page_count = pdf_doc.page_count
        for p in range(pdf_page_count):
            page = pdf_doc.load_page(p)
            text = page.get_text("text")
            pdf_pages_text.append(text.strip())
    except Exception as e:
        st.error(f"Failed to read PDF: {e}")
        st.stop()
else:
    # decode txt
    try:
        text = raw.decode("utf-8")
    except Exception:
        text = raw.decode("utf-8", errors="replace")
    text = text.replace('\r\n', '\n').replace('\r','\n')
    full_text = "\n".join(text.splitlines())
    pdf_pages_text = [full_text]
    pdf_page_count = 1

# Mode
mode = st.selectbox("Open mode", ["Read", "Append"])

# If PDF, force Read mode
if is_pdf:
    mode = "Read"

# Reader UI
st.markdown(READER_CSS, unsafe_allow_html=True)
st.subheader("Reader")
col1, col2 = st.columns([3,1])
with col1:
    st.markdown(f"**File:** {uploaded.name}")
with col2:
    st.markdown(f"**Mode:** {mode}")

# Initialize page_idx in session state
if "file_key" not in st.session_state or st.session_state["file_key"] != uploaded.name:
    st.session_state["file_key"] = uploaded.name
    st.session_state["page_idx"] = 0

# page navigation buttons
nav_col1, nav_col2, nav_col3 = st.columns([1,4,1])
with nav_col1:
    if st.button("← Prev"):
        if st.session_state["page_idx"] > 0:
            st.session_state["page_idx"] -= 1
with nav_col3:
    if st.button("Next →"):
        if st.session_state["page_idx"] < len(pdf_pages_text)-1:
            st.session_state["page_idx"] += 1
with nav_col2:
    st.markdown(f"Page {st.session_state.get('page_idx',0)+1} of {len(pdf_pages_text)}")

# Display current page in Kindle-style box
current_page_text = pdf_pages_text[st.session_state.get("page_idx",0)]
paras = [p for p in current_page_text.split("\n\n") if p.strip()]

reader_html = '<div class="reader">'
reader_html += '<div class="meta">Preview — {} — {} pages</div>'.format(uploaded.name, len(pdf_pages_text))
for p in paras:
    safe_p = p.replace("\n","<br/>")
    reader_html += f"<p>{safe_p}</p>"
reader_html += "</div>"

st.markdown(reader_html, unsafe_allow_html=True)

st.markdown("---")
# If txt and Append mode, show tools & editing
if is_txt and mode == "Append":
    st.subheader("String tools")
    col1, col2, col3, col4, col5 = st.columns(5)
    # Initialize session state for text content
    if "original_text" not in st.session_state or st.session_state.get("file_key") != uploaded.name:
        st.session_state["file_key"] = uploaded.name
        st.session_state["original_text"] = pdf_pages_text[0]
        st.session_state["current_text"] = st.session_state["original_text"]
        st.session_state["last_count"] = None

    with col1:
        if st.button("UPPERCASE"):
            st.session_state["current_text"] = text_utils.to_upper(st.session_state["current_text"])
            st.success("Converted to UPPERCASE.")
    with col2:
        if st.button("lowercase"):
            st.session_state["current_text"] = text_utils.to_lower(st.session_state["current_text"])
            st.success("Converted to lowercase.")
    with col3:
        if st.button("strip"):
            st.session_state["current_text"] = text_utils.strip_text(st.session_state["current_text"])
            st.success("Stripped leading/trailing whitespace.")
    with col4:
        if st.button("Capitalize"):
            st.session_state["current_text"] = text_utils.capitalize_text(st.session_state["current_text"])
            st.success("Capitalized first character of the text.")
    with col5:
        if st.button("Title Case"):
            st.session_state["current_text"] = text_utils.title_text(st.session_state["current_text"])
            st.success("Converted text to Title Case.")

    st.markdown("### Replace")
    c_old, c_new, c_btn = st.columns([3,3,1])
    old = c_old.text_input("Old substring", key="old_sub")
    new = c_new.text_input("New substring", key="new_sub")
    replace_clicked = c_btn.button("Replace")
    if replace_clicked:
        st.session_state["current_text"] = text_utils.replace_text(st.session_state["current_text"], old, new)
        st.success(f"Replaced all occurrences of '{old}' with '{new}'.")

    st.markdown("### Count substring")
    sub = st.text_input("Substring to count", key="count_sub")
    if st.button("Count"):
        cnt = text_utils.count_substring(st.session_state["current_text"], sub)
        st.session_state["last_count"] = cnt
        st.info(f"'{sub}' appears {cnt} times in the current text.")

    if st.session_state.get("last_count") is not None:
        st.write(f"Last count result: {st.session_state['last_count']}")
    st.markdown("---")
    st.subheader("Preview / Edit area")
    # Use editable text_area bound to the session_state value
    txt = st.text_area("Current text (editable)", value=st.session_state["current_text"], height=300, key="edit_area")
    # update current_text when user edits the text_area
    st.session_state["current_text"] = txt

    st.markdown("---")
    st.subheader("Save (Append mode only)")
    extra = st.text_area("Extra text to append", value="", height=120, key="extra_append")
    if st.button("Save & Download"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        final_text = st.session_state["current_text"]
        if extra:
            if not final_text.endswith("\n"):
                final_text += "\n"
            final_text += extra
        final_text += "\n\nProcessed on: " + timestamp + "\n"
        orig_name = Path(st.session_state["file_key"]).stem
        out_name = f"{orig_name}_edited.txt"
        st.download_button("Download edited file", data=final_text.encode('utf-8'), file_name=out_name, mime='text/plain')
        st.success("Prepared edited file for download.")
else:
    if not is_txt:
        st.info("PDF files are read-only in this app. Switch to a .txt file and Append mode to edit and save.")
    else:
        st.info("Append mode is required to edit/save .txt files. Switch to Append mode if you wish to edit.")

st.caption("String operation functions are kept in text_utils.py to keep UI logic separate.")
