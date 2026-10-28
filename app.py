import re
import math
from collections import Counter

import streamlit as st

st.set_page_config(page_title="Word Counter", page_icon="📝")
st.title("📝 WORD COUNTER")

if "text" not in st.session_state:
    st.session_state["text"] = ""
if "report" not in st.session_state:
    st.session_state["report"] = ""


def load_file():
    uploaded = st.session_state.get("uploaded")
    if uploaded is not None:
        try:
            st.session_state["text"] = uploaded.getvalue().decode("utf-8")
            st.session_state["report"] = ""
        except UnicodeDecodeError:
            st.session_state["file_error"] = True


def clear_all():
    st.session_state["text"] = ""
    st.session_state["report"] = ""


def build_report(text):
    words = re.findall(r"\b[\w']+\b", text.lower(), flags=re.UNICODE)
    characters = len(text)
    characters_without_spaces = sum(not c.isspace() for c in text)
    sentences = len(re.findall(r"[.!?]+", text))
    paragraphs = len([p for p in text.splitlines() if p.strip()])
    unique_words = len(set(words))
    frequency = Counter(words)
    reading_time = max(1, math.ceil(len(words) / 200))

    repeated = {w: c for w, c in frequency.most_common() if c > 1}

    lines = [
        "WORD COUNTER REPORT",
        "=" * 35,
        f"Total Words: {len(words)}",
        f"Total Characters: {characters}",
        f"Characters Without Spaces: {characters_without_spaces}",
        f"Total Sentences: {sentences}",
        f"Total Paragraphs: {paragraphs}",
        f"Unique Words: {unique_words}",
        f"Estimated Reading Time: {reading_time} minute(s)",
        "",
        "MOST FREQUENT WORDS",
        "-" * 35,
    ]

    for word, count in frequency.most_common(10):
        lines.append(f"{word}: {count}")

    lines.extend(["", "REPEATED WORDS", "-" * 35])

    if repeated:
        for word, count in repeated.items():
            lines.append(f"{word}: {count}")
    else:
        lines.append("No repeated words.")

    return "\n".join(lines)


st.file_uploader(
    "Open Text File (.txt)", type=["txt"], key="uploaded", on_change=load_file
)

if st.session_state.pop("file_error", False):
    st.error("Could not read this file. Please upload a UTF-8 .txt file.")

st.text_area("Enter or paste your text below:", key="text", height=250)

col1, col2 = st.columns(2)
with col1:
    analyze = st.button("Analyze Text", type="primary", use_container_width=True)
with col2:
    st.button("Clear", on_click=clear_all, use_container_width=True)

if analyze:
    if not st.session_state["text"].strip():
        st.warning("Please enter some text.")
    else:
        st.session_state["report"] = build_report(st.session_state["text"])

if st.session_state["report"]:
    st.subheader("Analysis Results")
    st.code(st.session_state["report"], language=None)
    st.download_button(
        "Save Report",
        data=st.session_state["report"],
        file_name="word_counter_report.txt",
        mime="text/plain",
    )