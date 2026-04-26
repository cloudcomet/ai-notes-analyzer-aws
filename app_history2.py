import streamlit as st
import boto3
import time
import os
import json
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
st.set_page_config(page_title="InsightNotes", layout="wide")

# -----------------------------
# SAFE SESSION INIT
# -----------------------------
defaults = {
    "messages": [],
    "summary": "",
    "file_name": "",
    "uploaded": False
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -----------------------------
# CSS (CLEAN PREMIUM)
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.chat-user {
    background: #2563eb;
    color: white;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
}

.chat-bot {
    background: #1e293b;
    color: white;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
}

.card {
    background: #111827;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
}

h1, h2, h3 {
    color: #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER (BRANDING)
# -----------------------------
st.markdown("# 🧠 InsightNotes")
st.caption("Turn documents into insights with AI")

# -----------------------------
# S3 HELPERS
# -----------------------------
def save_summary(file_name, summary):
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=f"history/{file_name}_summary.txt",
        Body=summary.encode("utf-8")
    )

def save_chat(file_name, messages):
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=f"history/{file_name}_chat.json",
        Body=json.dumps(messages).encode("utf-8")
    )

def load_chat(file_name):
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=f"history/{file_name}_chat.json")
        return json.loads(obj["Body"].read().decode())
    except:
        return []

def load_summary(file_name):
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=f"history/{file_name}_summary.txt")
        return obj["Body"].read().decode()
    except:
        return ""

def list_history():
    try:
        res = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix="history/")
        files = []
        for obj in res.get("Contents", []):
            key = obj["Key"]
            if key.endswith("_chat.json"):
                files.append(key.replace("history/", "").replace("_chat.json", ""))
        return list(set(files))
    except:
        return []

# -----------------------------
# SIDEBAR (HISTORY)
# -----------------------------
with st.sidebar:
    st.header("📂 History")

    history_files = list_history()

    if history_files:
        for f in history_files:
            if st.button(f"📄 {f}"):
                st.session_state.file_name = f
                st.session_state.uploaded = True
                st.session_state.messages = load_chat(f)
                st.session_state.summary = load_summary(f)
                st.rerun()
    else:
        st.write("No history yet")

    st.markdown("---")

    if st.button("🔄 Reset"):
        for key in ["messages", "summary", "file_name", "uploaded"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader(
    "📤 Upload Document",
    type=["pdf", "docx", "pptx", "txt"]
)

if uploaded_file:
    name = uploaded_file.name.replace(" ", "_")
    s3.upload_fileobj(uploaded_file, BUCKET_NAME, "uploads/" + name)

    st.success(f"Uploaded: {name}")

    st.session_state.file_name = name
    st.session_state.uploaded = True

    time.sleep(2)

# -----------------------------
# LOAD HISTORY
# -----------------------------
if st.session_state.file_name:
    if not st.session_state.get("messages"):
        st.session_state.messages = load_chat(st.session_state.file_name)

    if not st.session_state.get("summary"):
        st.session_state.summary = load_summary(st.session_state.file_name)

# -----------------------------
# FETCH PROCESSED TEXT
# -----------------------------
document_text = ""

if st.session_state.uploaded:
    key = f"processed/{st.session_state.file_name}.txt"

    for _ in range(15):
        try:
            res = s3.get_object(Bucket=BUCKET_NAME, Key=key)
            document_text = res["Body"].read().decode()
            break
        except:
            st.info("⏳ Processing document...")
            time.sleep(2)

# -----------------------------
# MAIN UI
# -----------------------------
if document_text:

    col1, col2 = st.columns([1, 2])

    # -------------------------
    # LEFT (SUMMARY FIRST)
    # -------------------------
    with col1:
        st.subheader("🧠 Summary")

        if not st.session_state.summary:
            with st.spinner("Generating summary..."):
                st.session_state.summary = summarize(document_text)
                save_summary(st.session_state.file_name, st.session_state.summary)

        st.markdown(f"<div class='card'>{st.session_state.summary}</div>", unsafe_allow_html=True)

        # Collapsible document preview
        with st.expander("📄 View Document"):
            st.write(document_text[:4000])

    # -------------------------
    # RIGHT (CHAT)
    # -------------------------
    with col2:
        st.subheader("💬 Chat")

        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"<div class='chat-user'>👤 {msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-bot'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

        user_input = st.chat_input("Ask something about your document...")

        if user_input:
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })

            with st.spinner("Thinking..."):
                answer = answer_question(document_text, user_input)

            placeholder = st.empty()
            full = ""

            for ch in answer:
                full += ch
                placeholder.markdown(f"<div class='chat-bot'>🤖 {full}</div>", unsafe_allow_html=True)
                time.sleep(0.002)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

            save_chat(st.session_state.file_name, st.session_state.messages)

            st.rerun()

# -----------------------------
# EMPTY STATE
# -----------------------------
else:
    st.info("📤 Upload a document to begin 🚀")
