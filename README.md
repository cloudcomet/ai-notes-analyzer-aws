# 🧠 InsightNotes

**Turn documents into insights with AI**

InsightNotes is an AI-powered web application that allows users to upload documents and interact with them through intelligent summarization and conversational querying. It transforms unstructured content into meaningful insights using modern cloud architecture and LLM APIs.

---

## 🚀 Features

* 📄 Upload documents (PDF, DOCX, PPTX, TXT)
* 🧠 AI-powered summarization
* 💬 Chat with your documents (context-aware)
* 🕘 Persistent chat history (saved on cloud)
* 📂 Resume previous sessions from sidebar
* ⚡ Fast document processing pipeline
* 🎨 Clean, modern UI (Streamlit-based)

---

## 🏗️ Architecture

```plaintext
User Upload → AWS S3 → Lambda Trigger → EC2 Processing → S3 (Processed Text)
                                      ↓
                                 Streamlit App
                                      ↓
                              AI API (OpenRouter)
```

---

## 🛠️ Tech Stack

### Frontend

* Streamlit (Python)

### Backend

* Python

### Cloud Services (AWS)

* S3 → Storage (uploads + processed + history)
* Lambda → Trigger processing
* EC2 → File parsing + app hosting
* SSM → Remote execution

### AI Integration

* OpenRouter API (LLM for summarization + Q&A)

---

## 📂 Project Structure

```plaintext
notes-app/
│
├── app.py              # Main frontend (UI + logic)
├── ai_module.py        # AI API integration
├── process.py          # File parsing (PDF, DOCX, PPTX, TXT)
├── requirements.txt
├── .env                # Environment variables (NOT pushed)
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/insightnotes.git
cd insightnotes
```

---

### 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_api_key
S3_BUCKET_NAME=your_bucket_name
AWS_REGION=ap-south-1
```

---

### 5️⃣ Run Application

```bash
streamlit run app.py
```

---

## ☁️ Deployment

* Hosted on AWS EC2
* Reverse proxy using Caddy (HTTPS enabled)
* Domain configured for public access
* Secure backend (localhost binding)

---

## 🔐 Security Practices

* Environment variables for sensitive data
* IAM roles for AWS access (no hardcoded keys)
* Reverse proxy to hide internal services
* No direct exposure of backend ports

---

## 🎯 Future Enhancements

* 🔍 Semantic search (RAG)
* ✨ Highlight answers inside documents
* 👥 Multi-user authentication
* 📊 Analytics dashboard
* 📁 Multi-document support

---

## 💡 Key Learnings

* Cloud-based system design (AWS)
* Serverless processing pipelines
* LLM integration using APIs
* Session persistence using S3
* UI/UX design with Streamlit

---

## 📌 Author

**Aum Vinod Singh**
B.E. Artificial Intelligence & Data Science

---

## ⭐ If you like this project, give it a star!
