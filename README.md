# 🧠 AI-Powered Smart Notes Analyzer

An end-to-end serverless application that allows users to upload documents and interact with them through AI-powered summarization and question answering.

---

## 🚀 Features

* 📄 Upload documents (PDF, DOCX, PPTX, TXT)
* 🔍 Automatic text extraction using AWS backend
* 🧠 AI-powered summarization
* 💬 Chat with your documents
* ☁️ Serverless processing pipeline (S3 + Lambda + EC2)
* 🌐 Deployed with custom domain and HTTPS

---

## 🏗️ Architecture

```
User Upload → AWS S3 → Lambda Trigger → EC2 Processing → S3 (Processed Text)
                                      ↓
                                 Streamlit App
                                      ↓
                               AI API (OpenRouter)
```

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### Cloud Services

* AWS S3 (Storage)
* AWS Lambda (Trigger)
* AWS EC2 (Processing + Hosting)
* AWS SSM (Remote execution)

### AI Integration

* OpenRouter API (LLM inference)

### Deployment

* Caddy (Reverse Proxy + HTTPS)
* Docker (optional)

---

## 📂 Project Structure

```
notes-app/
│
├── app.py              # Streamlit frontend
├── ai_module.py        # AI integration (OpenRouter)
├── process.py          # File parsing + extraction
├── requirements.txt
├── Dockerfile
├── .env                # Environment variables (NOT pushed)
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```
git clone https://github.com/YOUR_USERNAME/smart-notes-analyzer.git
cd smart-notes-analyzer
```

---

### 2. Create Virtual Environment

```
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 4. Setup Environment Variables

Create a `.env` file:

```
OPENROUTER_API_KEY=your_api_key
S3_BUCKET_NAME=your_bucket_name
AWS_REGION=ap-south-1
```

---

### 5. Run Application

```
streamlit run app.py
```

---

## 🐳 Docker (Optional)

Build and run:

```
docker build -t notes-app .
docker run -p 8501:8501 --env-file .env notes-app
```

---

## 🌐 Deployment

* Hosted on AWS EC2
* Reverse proxy using Caddy
* Automatic HTTPS enabled

---

## 🔐 Security Practices

* Environment variables for secrets
* IAM roles for AWS access
* Internal service isolation (localhost binding)
* No direct exposure of backend services

---

## 🎯 Future Improvements

* Vector database for semantic search
* Better document chunking
* Multi-document chat
* User authentication
* UI enhancements

---

## 💡 Key Learnings

* Serverless architecture design
* Cloud service integration (AWS)
* Handling large file processing pipelines
* API-based AI integration
* Deployment and production optimization

---

## 📌 Author

Aum Vinod Singh
B.E. Artificial Intelligence & Data Science

---

## ⭐ If you like this project, consider giving it a star!
