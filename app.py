import streamlit as st
import boto3
import time

from ai_module import summarize, answer_question

# -----------------------------
# CONFIG
# -----------------------------
BUCKET_NAME = "smart-notes-analyzer-cc"

s3 = boto3.client("s3")

# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="AI Notes Analyzer", layout="wide")
st.title("🧠 AI Smart Notes Analyzer")

# -----------------------------
# SESSION
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
# UPLOAD
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload your notes (PDF, DOCX, TXT)",
    type=["txt", "pptx",  "pdf", "docx"]
)

if uploaded_file:

    file_name = uploaded_file.name.replace(" ", "_")

    s3.upload_fileobj(
        uploaded_file,
        BUCKET_NAME,
        "uploads/" + file_name
    )

    st.success("✅ File uploaded! Processing...")

    st.session_state.file_uploaded = True
    st.session_state.file_name = file_name

    time.sleep(3)

# -----------------------------
# FETCH TEXT
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
        with st.spinner("Generating summary..."):
            st.session_state.summary = summarize(document_text)

    st.subheader("📄 Summary")
    st.success(st.session_state.summary)

# -----------------------------
# CHAT
# -----------------------------
if document_text:

    st.subheader("💬 Chat with your document")

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Ask something...")

    if user_input:

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        answer = answer_question(document_text, user_input)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()

# -----------------------------
# EMPTY
# -----------------------------
else:
    st.info("📤 Upload a document to begin")
