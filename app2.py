import streamlit as st
import boto3
import time
import os
from dotenv import load_dotenv

from ai_module import summarize, answer_question

# -----------------------------
# LOAD ENV
# -----------------------------
load_dotenv()
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

s3 = boto3.client("s3")

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Notes Analyzer", layout="wide")

# -----------------------------
# PREMIUM CSS
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.chat-user {
    background: #2563eb;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
}

.chat-bot {
    background: #1e293b;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
}

.sidebar .sidebar-content {
    background: #111827;
}

h1, h2, h3 {
    color: #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("# 🧠 Smart Notes AI")
st.caption("Upload → Analyze → Chat with your documents")

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.header("⚙️ Controls")

    if st.button("🔄 Reset"):
        st.session_state.clear()

    st.markdown("---")
    st.write("📄 Supported:")
    st.write("PDF, DOCX, PPTX, TXT")

# -----------------------------
# SESSION
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "file_name" not in st.session_state:
    st.session_state.file_name = ""

if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader(
    "📤 Upload Document",
    type=["pdf", "docx", "pptx", "txt"]
)

if uploaded_file:
    file_name = uploaded_file.name.replace(" ", "_")

    s3.upload_fileobj(uploaded_file, BUCKET_NAME, "uploads/" + file_name)

    st.success(f"Uploaded: {file_name}")

    st.session_state.file_name = file_name
    st.session_state.uploaded = True

    time.sleep(2)

# -----------------------------
# FETCH TEXT
# -----------------------------
document_text = ""

if st.session_state.uploaded:
    processed_key = "processed/" + st.session_state.file_name + ".txt"

    for _ in range(15):
        try:
            response = s3.get_object(Bucket=BUCKET_NAME, Key=processed_key)
            document_text = response['Body'].read().decode('utf-8')
            break
        except:
            st.info("⏳ Processing...")
            time.sleep(2)

# -----------------------------
# LAYOUT
# -----------------------------
if document_text:

    col1, col2 = st.columns([1, 2])

    # -------------------------
    # LEFT PANEL (DOC)
    # -------------------------
    with col1:
        st.subheader("📄 Document Preview")

        preview = document_text[:2000]

        st.text_area("Extracted Text", preview, height=500)

        if not st.session_state.summary:
            with st.spinner("Summarizing..."):
                st.session_state.summary = summarize(document_text)

        st.markdown("### 🧠 Summary")
        st.markdown(st.session_state.summary)

    # -------------------------
    # RIGHT PANEL (CHAT)
    # -------------------------
    with col2:
        st.subheader("💬 Chat")

        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"<div class='chat-user'>👤 {msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-bot'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

        user_input = st.chat_input("Ask something...")

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})

            with st.spinner("Thinking..."):
                answer = answer_question(document_text, user_input)

            # typing effect
            placeholder = st.empty()
            full_text = ""

            for char in answer:
                full_text += char
                placeholder.markdown(f"<div class='chat-bot'>🤖 {full_text}</div>", unsafe_allow_html=True)
                time.sleep(0.005)

            st.session_state.messages.append({"role": "assistant", "content": answer})

            st.rerun()

# -----------------------------
# EMPTY STATE
# -----------------------------
else:
    st.info("Upload a document to begin 🚀")

