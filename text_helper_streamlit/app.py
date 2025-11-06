import streamlit as st
from pathlib import Path
from datetime import datetime
import text_utils

st.set_page_config(page_title="Text Helper", layout="centered")

st.title("Text Helper — Streamlit App")

uploaded = st.file_uploader("Upload a .txt file", type=["txt"])

if not uploaded:
    st.info("Please upload a .txt file to get started.")
    st.stop()

# Validate extension (extra check)
suffix = Path(uploaded.name).suffix.lower()
if suffix != ".txt":
    st.error("Only .txt files are supported.")
    st.stop()

# Read file content (decoded)
try:
    original_text = uploaded.getvalue().decode("utf-8")
except Exception:
    # fallback
    original_text = uploaded.getvalue().decode("utf-8", errors="replace")

# Initialize session state
if "original_text" not in st.session_state or st.session_state.get("file_name") != uploaded.name:
    st.session_state["file_name"] = uploaded.name
    st.session_state["original_text"] = original_text
    st.session_state["current_text"] = original_text
    st.session_state["last_count"] = None

mode = st.selectbox("Open mode", ["Read", "Append"])

# Preview (first 20 lines)
lines = st.session_state["current_text"].splitlines()
preview_lines = lines[:20]
st.subheader("Preview (first 20 lines)")
st.code("\n".join(preview_lines) if preview_lines else "<empty file>")

# Stats
line_count = len(lines)
word_count = text_utils.word_count(st.session_state["current_text"])
char_count = len(st.session_state["current_text"])
st.write(f"**Lines:** {line_count}    **Words:** {word_count}    **Characters:** {char_count}")

st.markdown("---")
st.subheader("String tools")

col1, col2, col3 = st.columns(3)

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
# show full current text in a text_area for convenience (user can inspect, but we keep operations pure)
st.text_area("Current text (editable for preview only)", value=st.session_state["current_text"], height=200, key="preview_area", disabled=True)

st.markdown("---")
st.subheader("Save (Append mode only)")
if mode == "Read":
    st.info("Saving is disabled in Read mode.")
else:
    extra = st.text_area("Extra text to append", value="", height=120, key="extra_append")
    if st.button("Save & Download"):
        # prepare final text: current_text (after operations) + appended text + timestamp line
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        final_text = st.session_state["current_text"]
        if extra:
            # ensure proper newline separation
            if not final_text.endswith("\n"):
                final_text += "\n"
            final_text += extra
        final_text += "\n\nProcessed on: " + timestamp + "\n"
        # create a filename
        orig_name = Path(st.session_state["file_name"]).stem
        out_name = f"{orig_name}_edited.txt"
        st.download_button("Download edited file", data=final_text.encode('utf-8'), file_name=out_name, mime='text/plain')
        st.success("Prepared edited file for download.")

st.markdown("---")
st.caption("String operation functions are kept in text_utils.py to keep UI logic separate.")
