# rag_pipeline.py — Neubaitics AI Customer Support RAG Pipeline
# Production-ready: LangChain + FAISS + Groq LLM + HuggingFace Embeddings
 
import os
import json
from datetime import datetime
from dotenv import load_dotenv
 
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
 
load_dotenv()
 
# ─── INTENT CATEGORIES ────────────────────────────────────────────────────────
INTENT_PATTERNS = {
    "pricing":       ["price", "cost", "fee", "charge", "quote", "pricing", "rate", "afford", "budget", "how much", "₹", "rupee"],
    "services":      ["service", "offer", "provide", "product", "solution", "build", "develop", "create", "make", "chatbot", "video analytics", "iot", "robotics", "generative"],
    "onboarding":    ["onboard", "start", "begin", "process", "how do i", "get started", "sign up", "join", "setup", "timeline", "how long"],
    "training":      ["train", "course", "learn", "internship", "program", "study", "education", "ml", "deep learning", "certification"],
    "contact":       ["contact", "reach", "call", "email", "phone", "address", "location", "visit", "talk to", "speak with", "human"],
    "support":       ["help", "issue", "problem", "bug", "error", "broken", "not working", "support", "fix", "trouble"],
    "company":       ["about", "who are", "neubaitics", "company", "team", "founded", "history", "background"],
    "lead":          ["interested", "want to", "would like", "i need", "looking for", "proposal", "demo", "schedule", "book"],
    "escalation":    ["urgent", "asap", "immediately", "critical", "emergency", "escalate"],
}
 
def detect_intent(user_input: str) -> str:
    """Detect the primary intent of a user message."""
    text = user_input.lower()
    scores = {intent: 0 for intent in INTENT_PATTERNS}
    for intent, keywords in INTENT_PATTERNS.items():
        for kw in keywords:
            if kw in text:
                scores[intent] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "general"
 
 
def load_documents():
    """Load company and FAQ knowledge base documents."""
    loader1 = TextLoader("data/company.txt", encoding="utf-8")
    loader2 = TextLoader("data/faq.txt", encoding="utf-8")
    return loader1.load() + loader2.load()
 
 
def split_documents(documents):
    """Split documents into overlapping chunks for better retrieval."""
    splitter = CharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=80,
        separator="\n"
    )
    return splitter.split_documents(documents)
 
 
def create_vectorstore(docs):
    """Create or load FAISS vector store with HuggingFace embeddings."""
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )
    db = FAISS.from_documents(docs, embeddings)
    db.save_local("vector_store/neubaitics_faiss")
    return db
 
 
def get_llm():
    """Initialize Groq LLM with controlled temperature for factual accuracy."""
    return ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant",
        temperature=0.2,
        max_tokens=512
    )
 
 
def build_prompt_template():
    """Create a professional, company-specific prompt template."""
    template = """You are a professional AI customer support assistant for Neubaitics Tech Private Limited — an AI, Robotics, and IoT company based in Chennai, India.
 
Your role is to:
- Answer customer questions accurately using the provided context
- Be helpful, professional, and concise
- Direct customers to human support when needed (email: info@neubaitics.com | phone: +91-9791729777)
- Never make up information not present in the context
 
Context from Neubaitics Knowledge Base:
{context}
 
Customer Question: {question}
 
Instructions:
- Answer only from the context provided above
- If the answer is not in the context, say: "I don't have specific information on that. Please contact our team at info@neubaitics.com or call +91-9791729777 for a detailed answer."
- Keep responses clear and professional (2-4 sentences for simple questions, more detail for complex ones)
- End with a helpful follow-up offer when appropriate
 
Assistant Answer:"""
 
    return PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )
 
 
def create_rag_chain():
    """Build and return the complete production RAG pipeline."""
    documents = load_documents()
    docs = split_documents(documents)
    db = create_vectorstore(docs)
 
    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )
 
    llm = get_llm()
    prompt = build_prompt_template()
 
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
 
    return qa_chain
 
 
def save_chat_log(user_msg: str, bot_msg: str, intent: str):
    """Persist chat history to JSONL file for analysis and improvement."""
    os.makedirs("leads", exist_ok=True)
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "intent": intent,
        "user": user_msg,
        "bot": bot_msg
    }
    with open("leads/chat_history.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
 
 
def is_escalation_needed(answer: str) -> bool:
    """Check if the AI response requires human escalation."""
    low_confidence_signals = [
        "i don't know",
        "i don't have specific information",
        "i cannot",
        "i'm not sure",
        "please contact"
    ]
    if len(answer.strip()) < 25:
        return True
    answer_lower = answer.lower()
    return any(sig in answer_lower for sig in low_confidence_signals)
 
 
def get_escalation_message() -> str:
    return (
        "🔔 **This query needs human attention.** "
        "Please reach out to our support team:\n\n"
        "📧 **Email:** info@neubaitics.com\n"
        "📞 **Phone:** +91-9791729777\n"
        "🌐 **Website:** [www.neubaitics.com](https://www.neubaitics.com)\n\n"
        "Our team responds within **24 business hours**."
    )
