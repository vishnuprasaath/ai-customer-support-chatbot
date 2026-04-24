# 🤖 Neubaitics AI Customer Support Automation System

> **Production-ready AI support chatbot** built for Neubaitics Tech Private Limited.
> Powered by LangChain · FAISS · Groq LLaMA 3.1 · HuggingFace Embeddings · Streamlit

---

## 📋 Project Overview

This system is an **AI-powered customer support automation platform** that handles common customer queries about Neubaitics' services, pricing, onboarding, and training programs — without manual intervention.

### Problem Solved
Manual handling of repetitive customer queries leads to delays, increased workload, and inconsistent responses. This system:
- ✅ Answers queries **instantly** using the company knowledge base
- ✅ Provides **context-aware** responses (not keyword matching)
- ✅ **Escalates** to human support when confidence is low
- ✅ **Captures leads** automatically from interested visitors
- ✅ **Logs all chats** for future model improvement

---

## 🏗️ Architecture

```
User Query
    │
    ▼
Intent Detection (rule-based, 9 categories)
    │
    ▼
RAG Pipeline (LangChain RetrievalQA)
    ├── FAISS Vector Store (HuggingFace all-MiniLM-L6-v2 embeddings)
    │       └── company.txt + faq.txt → chunked → embedded → indexed
    └── Groq LLM (LLaMA 3.1 8B Instant)
            └── Custom prompt template → grounded, professional answer
    │
    ▼
Escalation Check → Human Support if low confidence
    │
    ▼
Streamlit UI (Chat + FAQ Panel + Lead Capture + History)
    │
    ▼
Chat Log (leads/chat_history.jsonl) + Leads (leads/leads.csv)
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **UI Framework** | Streamlit 1.35+ |
| **LLM** | Groq API — LLaMA 3.1 8B Instant |
| **Embeddings** | HuggingFace `all-MiniLM-L6-v2` |
| **Vector DB** | FAISS (local, CPU) |
| **Orchestration** | LangChain RetrievalQA |
| **Intent Detection** | Rule-based keyword matching (9 intents) |
| **Data Persistence** | CSV (leads) + JSONL (chat history) |

---

## 📁 Project Structure

```
neubaitics_support/
├── app.py                  # Streamlit frontend (main entry point)
├── main.py                 # RAG pipeline + intent detection + utilities
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── README.md               # This file
│
├── data/
│   ├── company.txt         # Company knowledge base
│   └── faq.txt             # FAQ knowledge base (20 Q&As)
│
├── vector_store/           # Auto-created: FAISS index files
│   └── neubaitics_faiss/
│
└── leads/                  # Auto-created: persisted data
    ├── leads.csv           # Lead capture records
    └── chat_history.jsonl  # All chat logs for analysis
```

---

## 🚀 Setup Guide

### Prerequisites
- Python 3.10 or higher
- A free Groq API key from [console.groq.com](https://console.groq.com)

### Step 1: Clone / Download the project
```bash
git clone <your-repo-url>
cd neubaitics_support
```

### Step 2: Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure environment variables
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### Step 5: Run the app
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## ✨ Features

### 1. AI Chat with RAG
- Retrieves relevant context from company + FAQ knowledge base
- Generates grounded, factual answers using LLaMA 3.1
- Shows source documents for transparency

### 2. Intent Detection (9 Categories)
`pricing` · `services` · `onboarding` · `training` · `contact` · `support` · `company` · `lead` · `escalation`

### 3. Top 10 FAQ Panel
Quick-access expandable FAQ panel alongside the chatbot — click "Ask this" to auto-fill any FAQ into the chat.

### 4. Chat History Sidebar
- Shows past queries with timestamps in the sidebar (like ChatGPT-style history)
- Counts total queries and escalations

### 5. Lead Capture
- Auto-triggered when user expresses interest or mentions contact/demo/pricing
- Collects name, email, company, area of interest, and requirement
- Saved to `leads/leads.csv` with timestamps

### 6. Escalation System
- Detects low-confidence answers (short, uncertain, or "I don't know")
- Serves a professional escalation message with contact details
- Tracks escalation rate in the sidebar stats

### 7. Contact Us Panel
Sidebar button reveals:
- 📧 Email with clickable mailto link
- 📞 Phone with clickable tel link
- 🌐 Website with external link

### 8. Chat Log Persistence
All conversations saved to `leads/chat_history.jsonl` with:
- Timestamp, intent, user message, bot response
- Use for model fine-tuning and business analytics

---

## 🔧 Customisation

### Update Knowledge Base
Edit `data/company.txt` and `data/faq.txt` with your latest content. Delete `vector_store/` folder and restart — the index will be rebuilt automatically.

### Change LLM Model
In `main.py`, change `model_name` in `get_llm()`:
```python
model_name="llama-3.3-70b-versatile"  # More powerful
model_name="gemma2-9b-it"             # Alternative
```

### Add More Intents
In `main.py`, extend `INTENT_PATTERNS` dict with new categories and keywords.

---

## 📊 Business Value

| Metric | Before AI | After AI |
|--------|-----------|----------|
| Response time | Hours | < 3 seconds |
| Support coverage | Business hours | 24/7 |
| Query handling capacity | Limited by staff | Unlimited |
| Lead capture rate | Manual | Automated |
| Consistency | Variable | 100% consistent |

---

## 🔒 Data Privacy

- All data stored locally — no data sent to external servers except the LLM API call
- Chat logs and leads are stored in plain files for easy export/deletion
- No personal data stored without user's explicit input (lead form)

---

## 🏢 About Neubaitics

**Neubaitics Tech Private Limited** | Chennai & Salem, Tamil Nadu, India
AI · Robotics · IoT | Anna University Incubated Startup

📧 info@neubaitics.com | 📞 +91-9791729777 | 🌐 www.neubaitics.com

## AUTHOR: VISHNUPRASAATH MUKUNTHAN vishnuprasaath2005@gmail.com 
