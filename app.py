# app.py — NeubAItics AI Customer Support System
# Light Mode · Clean Responsive UI · Production-Ready

import os
import csv
import time
import streamlit as st
from datetime import datetime
from main import (
    create_rag_chain,
    detect_intent,
    save_chat_log,
    is_escalation_needed,
    get_escalation_message,
)

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NeubAItics AI Support",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── LIGHT MODE CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

.stApp {
    background-color: #f5f7fa !important;
}

[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1rem;
}

.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 1.5rem !important;
    max-width: 1400px !important;
}

/* ── Bubbles ── */
.user-bubble {
    background: #1d4ed8;
    border-radius: 18px 18px 4px 18px;
    padding: 11px 16px;
    margin: 4px 0 4px auto;
    color: #ffffff;
    max-width: 82%;
    font-size: 0.9rem;
    line-height: 1.55;
    box-shadow: 0 2px 8px rgba(29,78,216,0.18);
    word-wrap: break-word;
}

.bot-bubble {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 18px 18px 18px 4px;
    padding: 11px 16px;
    margin: 4px auto 4px 0;
    color: #1e293b;
    max-width: 88%;
    font-size: 0.9rem;
    line-height: 1.6;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    word-wrap: break-word;
}

/* ── Intent badge ── */
.intent-badge {
    display: inline-block;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    color: #1d4ed8;
    font-size: 0.67rem;
    padding: 2px 9px;
    border-radius: 20px;
    margin-left: 4px;
    font-family: 'DM Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 500;
    vertical-align: middle;
}

/* ── Stat boxes ── */
.stat-box {
    background: #f0f9ff;
    border: 1px solid #bae6fd;
    border-radius: 10px;
    padding: 10px 8px;
    text-align: center;
}
.stat-num {
    font-size: 1.5rem;
    font-weight: 700;
    color: #0369a1;
    line-height: 1.1;
}
.stat-label {
    font-size: 0.67rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-top: 2px;
}

/* ── History ── */
.history-entry {
    background: #f8fafc;
    border-left: 3px solid #bfdbfe;
    border-radius: 0 6px 6px 0;
    padding: 7px 10px;
    margin: 4px 0;
    font-size: 0.77rem;
    color: #475569;
}

/* ── Contact card ── */
.contact-card {
    background: #f0f9ff;
    border: 1px solid #bae6fd;
    border-radius: 12px;
    padding: 14px;
    margin: 8px 0;
}
.contact-row {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid #e0f2fe;
    font-size: 0.83rem;
    color: #1e293b;
}
.contact-row:last-child { border-bottom: none; }
.contact-label {
    font-size: 0.67rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 2px;
}
.contact-val a {
    color: #1d4ed8;
    text-decoration: none;
    font-weight: 500;
}
.contact-val a:hover { text-decoration: underline; }

/* ── Welcome card ── */
.welcome-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-top: 3px solid #1d4ed8;
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 14px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}

/* ── Source card ── */
.source-card {
    background: #f8fafc;
    border-left: 3px solid #1d4ed8;
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    margin: 6px 0;
    font-size: 0.78rem;
    color: #475569;
    line-height: 1.5;
}

/* ── Section label ── */
.section-label {
    font-size: 0.71rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    font-weight: 600;
    margin-bottom: 8px;
    padding-bottom: 4px;
    border-bottom: 1px solid #f1f5f9;
}

/* ── Buttons ── */
.stButton > button {
    background: #1d4ed8 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 0.45rem 1rem !important;
    transition: background 0.15s ease, box-shadow 0.15s ease !important;
}
.stButton > button:hover {
    background: #1e40af !important;
    box-shadow: 0 4px 12px rgba(29,78,216,0.25) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea textarea {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
    color: #1e293b !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: #1d4ed8 !important;
    box-shadow: 0 0 0 3px rgba(29,78,216,0.1) !important;
    outline: none !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    margin-bottom: 5px !important;
}
[data-testid="stExpander"] summary {
    font-size: 0.82rem !important;
    color: #334155 !important;
    font-weight: 500 !important;
}
[data-testid="stExpander"] summary:hover {
    background: #f8fafc !important;
    border-radius: 8px !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] textarea {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    color: #1e293b !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Selectbox ── */
[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
    color: #1e293b !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

hr { border-color: #f1f5f9 !important; margin: 0.6rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
for key, default in {
    "chat_history": [],
    "session_history": [],
    "collect_lead": False,
    "show_contact": False,
    "query_count": 0,
    "escalation_count": 0,
    "last_sources": [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

os.makedirs("leads", exist_ok=True)

# ─── RAG CHAIN ────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading AI knowledge base...")
def load_chain():
    return create_rag_chain()

qa_chain = load_chain()

# ─── FAQ DATA ─────────────────────────────────────────────────────────────────
TOP_FAQS = [
    {"q": "What services does NeubAItics offer?",
     "a": "AI Video Analytics, Generative AI, Robotics & IoT, and AI/ML Training programs."},
    {"q": "How much does a custom AI chatbot cost?",
     "a": "Chatbot solutions start at Rs.75,000 for setup + monthly maintenance."},
    {"q": "What industries does NeubAItics serve?",
     "a": "Retail, Manufacturing, Healthcare, Smart Cities, and Education."},
    {"q": "How do I get started with NeubAItics?",
     "a": "Email us at contact@neubaitics.com for a free 30-minute consultation."},
    {"q": "Do you offer internship programs?",
     "a": "Yes! Stipend-based internships in AI, ML, and Embedded Systems are available."},
    {"q": "What is AI Video Analytics?",
     "a": "Computer vision for theft detection, face recognition, and behavior analytics."},
    {"q": "Do you offer AI/ML training courses?",
     "a": "Yes — individual courses from Rs.5,000; corporate batches from Rs.25,000/person."},
    {"q": "How long does a project take?",
     "a": "Chatbots: 2-4 weeks. Video analytics: 6-10 weeks. IoT/Robotics: 8-16 weeks."},
    {"q": "Is post-deployment support included?",
     "a": "Yes — Mon-Sat 9AM-6PM IST; 24/7 emergency support for enterprise clients."},
    {"q": "What technologies does NeubAItics use?",
     "a": "Python, TensorFlow, PyTorch, LangChain, FAISS, OpenCV, NVIDIA Jetson, AWS/Azure."},
]

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    st.markdown("""
    <div style="padding:4px 0 16px; text-align:center;">
        <div style="font-size:1.35rem; font-weight:700; color:#1d4ed8;">
            🤖 NeubAItics
        </div>
        <div style="font-size:0.69rem; color:#94a3b8; letter-spacing:0.12em;
                    text-transform:uppercase; margin-top:3px;">
            AI Support Assistant
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Stats
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-num">{st.session_state.query_count}</div>
            <div class="stat-label">Queries</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-num">{st.session_state.escalation_count}</div>
            <div class="stat-label">Escalated</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # History
    st.markdown('<div class="section-label">📂 Chat History</div>', unsafe_allow_html=True)

    if st.session_state.session_history:
        for entry in reversed(st.session_state.session_history[-12:]):
            q_text   = entry["q"]
            truncated = q_text[:40] + "…" if len(q_text) > 40 else q_text
            ts       = entry.get("ts", "")
            intent   = entry.get("intent", "")
            intent_html = f'<span style="color:#1d4ed8; font-weight:500;">{intent}</span>' if intent else ""
            st.markdown(f"""
            <div class="history-entry">
                <span style="font-size:0.67rem; color:#94a3b8;">{ts}{' · ' + intent_html if intent else ''}</span><br>
                {truncated}
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#f8fafc; border-radius:8px; padding:14px;
                    text-align:center; color:#94a3b8; font-size:0.79rem;
                    border:1px dashed #e2e8f0; line-height:1.6;">
            Your chat history<br>will appear here
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Contact Us
    if st.button("📞 Contact Us", use_container_width=True):
        st.session_state.show_contact = not st.session_state.show_contact

    if st.session_state.show_contact:
        st.markdown("""
        <div class="contact-card">
            <div style="font-weight:600; color:#1e293b; font-size:0.87rem; margin-bottom:10px;">
                Get in touch with us
            </div>
            <div class="contact-row">
                <span>📧</span>
                <div>
                    <div class="contact-label">Drop us a line at</div>
                    <div class="contact-val">
                        <a href="mailto:info@neubaitics.com">info@neubaitics.com</a>
                    </div>
                </div>
            </div>
            <div class="contact-row">
                <span>📞</span>
                <div>
                    <div class="contact-label">Give us a ring at</div>
                    <div class="contact-val">
                        <a href="tel:+919791729777">+91-9791729777</a>
                    </div>
                </div>
            </div>
            <div class="contact-row">
                <span>🌐</span>
                <div>
                    <div class="contact-label">Explore our world at</div>
                    <div class="contact-val">
                        <a href="https://www.neubaitics.com" target="_blank">www.neubaitics.com</a>
                    </div>
                </div>
            </div>
            <div style="margin-top:10px; font-size:0.7rem; color:#94a3b8; text-align:center;">
                Mon–Sat &nbsp;·&nbsp; 9 AM – 5 PM IST<br>Chennai, Tamil Nadu
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    ca, cb = st.columns(2)
    with ca:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.collect_lead = False
            st.rerun()
    with cb:
        if st.button("📥 Demo", use_container_width=True):
            st.session_state.collect_lead = True

    st.markdown("""
    <div style="margin-top:20px; font-size:0.67rem; color:#cbd5e1;
                text-align:center; line-height:1.65;">
        LangChain &nbsp;·&nbsp; FAISS &nbsp;·&nbsp; Groq LLaMA<br>
        <span style="color:#94a3b8;">© 2026 Vishnuprasaath Mukunthan.</span>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center; padding:4px 0 18px;">
    <h1 style="font-size:1.85rem; font-weight:700; color:#1e293b; margin:0 0 6px;">
        🤖 NeubAItics AI Support Assistant
    </h1>
    <p style="color:#64748b; font-size:0.88rem; margin:0 0 12px;">
        Intelligent customer support powered by RAG
        &nbsp;·&nbsp; Ask about services, pricing, onboarding &amp; more
    </p>
    <div style="display:inline-flex; gap:8px; flex-wrap:wrap; justify-content:center;">
        <span style="background:#eff6ff; border:1px solid #bfdbfe; color:#1d4ed8;
                     font-size:0.71rem; padding:3px 11px; border-radius:20px;">
            ⚡ Instant Answers
        </span>
        <span style="background:#f0fdf4; border:1px solid #bbf7d0; color:#16a34a;
                     font-size:0.71rem; padding:3px 11px; border-radius:20px;">
            🧠 Context-Aware RAG
        </span>
        <span style="background:#fefce8; border:1px solid #fef08a; color:#ca8a04;
                     font-size:0.71rem; padding:3px 11px; border-radius:20px;">
            🔔 Smart Escalation
        </span>
        <span style="background:#fdf4ff; border:1px solid #e9d5ff; color:#7c3aed;
                     font-size:0.71rem; padding:3px 11px; border-radius:20px;">
            📩 Lead Capture
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Two-column layout ─────────────────────────────────────────────────────────
chat_col, faq_col = st.columns([3, 1.25], gap="medium")

# ══════════════════════════════════════════════════════════════════════════════
# FAQ PANEL
# ══════════════════════════════════════════════════════════════════════════════
with faq_col:
    st.markdown("""
    <div style="background:#ffffff; border:1px solid #e2e8f0;
                border-top:3px solid #f59e0b; border-radius:10px;
                padding:12px 14px 8px; margin-bottom:8px;">
        <div style="font-size:0.8rem; font-weight:600; color:#1e293b;
                    letter-spacing:0.02em;">
            ⚡ Top 10 FAQs
        </div>
        <div style="font-size:0.72rem; color:#94a3b8; margin-top:2px;">
            Click to expand · Ask directly
        </div>
    </div>""", unsafe_allow_html=True)

    for i, faq in enumerate(TOP_FAQS):
        with st.expander(faq["q"], expanded=False):
            st.markdown(f"""
            <div style="color:#475569; font-size:0.82rem; line-height:1.55;
                        padding:4px 0 6px;">
                {faq['a']}
            </div>""", unsafe_allow_html=True)
            if st.button("💬 Ask this", key=f"faq_{i}", use_container_width=True):
                st.session_state["faq_prefill"] = faq["q"]
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# CHAT PANEL
# ══════════════════════════════════════════════════════════════════════════════
with chat_col:

    # Welcome banner (only when chat is empty)
    if not st.session_state.chat_history:
        st.markdown("""
        <div class="welcome-card">
            <div style="font-size:1rem; font-weight:600; color:#1e293b; margin-bottom:8px;">
                👋 Welcome to NeubAItics Support!
            </div>
            <div style="color:#64748b; font-size:0.84rem; line-height:1.6; margin-bottom:12px;">
                I'm your AI assistant, trained on NeubAItics' complete knowledge base.
                Here's what I can help you with:
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                <div style="background:#f8fafc; border-radius:8px; padding:10px 12px;
                            border:1px solid #e2e8f0; font-size:0.8rem; color:#475569;">
                    💼 <b style="color:#1e293b;">Services &amp; Pricing</b><br>
                    AI, Robotics, IoT solutions
                </div>
                <div style="background:#f8fafc; border-radius:8px; padding:10px 12px;
                            border:1px solid #e2e8f0; font-size:0.8rem; color:#475569;">
                    🚀 <b style="color:#1e293b;">Onboarding Process</b><br>
                    How to get started
                </div>
                <div style="background:#f8fafc; border-radius:8px; padding:10px 12px;
                            border:1px solid #e2e8f0; font-size:0.8rem; color:#475569;">
                    🎓 <b style="color:#1e293b;">Training Programs</b><br>
                    AI/ML courses &amp; internships
                </div>
                <div style="background:#f8fafc; border-radius:8px; padding:10px 12px;
                            border:1px solid #e2e8f0; font-size:0.8rem; color:#475569;">
                    🛠️ <b style="color:#1e293b;">Technical Support</b><br>
                    Post-deployment help
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    # Chat messages
    chat_box = st.container(height=420)
    with chat_box:
        for msg in st.session_state.chat_history:
            role    = msg["role"]
            content = msg["content"]
            intent  = msg.get("intent", "")

            if role == "user":
                st.markdown(f"""
                <div style="display:flex; justify-content:flex-end; margin:6px 0;">
                    <div>
                        <div style="text-align:right; font-size:0.67rem;
                                    color:#94a3b8; margin-bottom:3px;">You</div>
                        <div class="user-bubble">{content}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                badge = f'<span class="intent-badge">🎯 {intent}</span>' if intent else ""
                st.markdown(f"""
                <div style="margin:6px 0;">
                    <div style="font-size:0.67rem; color:#94a3b8; margin-bottom:3px;">
                        🤖 NeubAItics AI {badge}
                    </div>
                    <div class="bot-bubble">{content}</div>
                </div>""", unsafe_allow_html=True)

    # Source documents
    if st.session_state.last_sources:
        with st.expander("📄 View Source Documents", expanded=False):
            for i, doc in enumerate(st.session_state.last_sources[:3], 1):
                preview = doc.page_content[:260]
                if len(doc.page_content) > 260:
                    preview += "…"
                st.markdown(f"""
                <div class="source-card">
                    <b style="color:#1d4ed8; font-size:0.75rem;">Source {i}</b><br>
                    {preview}
                </div>""", unsafe_allow_html=True)

    # Chat input
    prefill    = st.session_state.pop("faq_prefill", "")
    user_input = st.chat_input("Ask me anything about NeubAItics…")
    if prefill and not user_input:
        user_input = prefill

    if user_input:
        intent = detect_intent(user_input)
        st.session_state.query_count += 1

        with st.spinner("Thinking…"):
            try:
                response = qa_chain.invoke({"query": user_input})
                answer   = response["result"]
                sources  = response.get("source_documents", [])
                if is_escalation_needed(answer):
                    answer = get_escalation_message()
                    st.session_state.escalation_count += 1
            except Exception:
                answer  = get_escalation_message()
                sources = []
                st.session_state.escalation_count += 1

        lead_triggers = ["contact", "interested", "demo", "proposal",
                         "want to", "pricing", "quote", "get started"]
        if any(t in user_input.lower() for t in lead_triggers):
            st.session_state.collect_lead = True

        st.session_state.chat_history.append(
            {"role": "user", "content": user_input, "intent": ""})
        st.session_state.chat_history.append(
            {"role": "assistant", "content": answer, "intent": intent})
        st.session_state.last_sources = sources

        ts = datetime.now().strftime("%H:%M")
        st.session_state.session_history.append(
            {"q": user_input, "ts": ts, "intent": intent})
        save_chat_log(user_input, answer, intent)
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# LEAD CAPTURE FORM
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.collect_lead:
    st.markdown("""
    <div style="background:#ffffff; border:1px solid #e2e8f0;
                border-top:3px solid #1d4ed8; border-radius:12px;
                padding:22px 26px 10px; margin-top:20px;
                box-shadow:0 2px 12px rgba(0,0,0,0.05);">
        <div style="font-size:1.05rem; font-weight:700; color:#1e293b; margin-bottom:4px;">
            📩 Connect with Our Team
        </div>
        <div style="color:#64748b; font-size:0.83rem; margin-bottom:16px;">
            Leave your details and we'll craft a solution tailored just for you.
            We respond within <b style="color:#1e293b;">24 business hours</b>.
        </div>
    </div>""", unsafe_allow_html=True)

    lc1, lc2 = st.columns(2)
    with lc1:
        name  = st.text_input("Your Name *",       placeholder="e.g. Arjun Kumar")
        email = st.text_input("Email Address *",   placeholder="arjun@company.com")
        phone = st.text_input("Contact Number *",  placeholder="e.g. +91-9876543210")
    with lc2:
        company  = st.text_input("Company / Organisation", placeholder="Your company name")
        interest = st.selectbox("Area of Interest", [
            "Select…",
            "AI Video Analytics",
            "Custom AI Chatbot",
            "Generative AI Solutions",
            "Robotics & IoT",
            "AI/ML Training Program",
            "Internship",
            "Other",
        ])

    requirement = st.text_area(
        "Describe Your Requirement",
        placeholder="Tell us briefly what you're looking to build or solve…",
        height=90
    )

    def sanitize(f):
        return str(f).replace('\n', ' ').replace('\r', ' ').replace(',', ' ').strip()

    sb1, sb2, _ = st.columns([1.2, 1, 4])
    with sb1:
        if st.button("🚀 Submit Enquiry", use_container_width=True):
            if name and email and phone:
                with open("leads/leads.csv", "a", newline='', encoding='utf-8') as f:
                    csv.writer(f).writerow([
                        datetime.now().strftime("%Y-%m-%d %H:%M"),
                        sanitize(name), sanitize(email),
                        sanitize(phone),
                        sanitize(company), sanitize(interest),
                        sanitize(requirement)
                    ])
                st.success("✅ Thank you for reaching out! Our team has received your enquiry and will get back to you shortly. We typically respond within 24 business hours — speak soon! 🚀")
                st.balloons()
                time.sleep(3)
                st.session_state.collect_lead = False
                st.rerun()
            else:
                st.error("Please fill in your name, email address, and contact number.")
    with sb2:
        if st.button("✕ Close", use_container_width=True):
            st.session_state.collect_lead = False
            st.rerun()

            