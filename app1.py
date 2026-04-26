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
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
}

.chat-message {
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
}

.user-msg {
    background-color: #1f77b4;
    color: white;
}

.bot-msg {
    background-color: #2c2f33;
    color: white;
}

.stButton>button {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
# 🧠 AI Smart Notes Analyzer
### Chat with your documents like ChatGPT
""")

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.header("⚙️ Controls")

    if st.button("🔄 Reset Chat"):
        st.session_state.messages = []
        st.session_state.summary = ""

    st.markdown("---")
    st.write("📄 Supported Files:")
    st.write("- PDF")
    st.write("- DOCX")
    st.write("- PPTX")
    st.write("- TXT")

# -----------------------------
# SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False

if "file_name" not in st.session_state:
    st.session_state.file_name = ""

if "summary" not in st.session_state:
    st.session_state.summary = ""

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader(
    "📤 Upload Document",
    type=["pdf", "docx", "pptx", "txt"],
    help="Upload notes to analyze"
)

if uploaded_file:

    file_name = uploaded_file.name.replace(" ", "_")

    s3.upload_fileobj(
        uploaded_file,
        BUCKET_NAME,
        "uploads/" + file_name
    )

    st.success(f"✅ Uploaded: {file_name}")

    st.session_state.file_uploaded = True
    st.session_state.file_name = file_name

    time.sleep(2)

# -----------------------------
# FETCH PROCESSED TEXT
# -----------------------------
document_text = ""

if st.session_state.file_uploaded:

    processed_key = "processed/" + st.session_state.file_name + ".txt"

    for _ in range(15):
        try:
            response = s3.get_object(
                Bucket=BUCKET_NAME,
                Key=processed_key
            )

            document_text = response['Body'].read().decode('utf-8')
            break

        except:
            st.info("⏳ Processing document...")
            time.sleep(2)

# -----------------------------
# SUMMARY
# -----------------------------
if document_text:

    if not st.session_state.summary:
        with st.spinner("🧠 Generating summary..."):
            st.session_state.summary = summarize(document_text)

    st.markdown("## 📄 Summary")

    st.markdown(f"""
    <div class="chat-message bot-msg">
    {st.session_state.summary}
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# CHAT
# -----------------------------
if document_text:

    st.markdown("## 💬 Chat with your document")

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-msg">
            👤 {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-msg">
            🤖 {msg["content"]}
            </div>
            """, unsafe_allow_html=True)

    user_input = st.chat_input("Ask something about your document...")

    if user_input:

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.spinner("🤖 Thinking..."):
            answer = answer_question(document_text, user_input)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()

# -----------------------------
# EMPTY STATE
# -----------------------------
else:
    st.info("📤 Upload a document to begin")
