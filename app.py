import streamlit as st
import fitz  # PyMuPDF
from groq import Groq
import base64
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Page config
st.set_page_config(
    page_title="Cricket Agent",
    page_icon="🏏",
    layout="centered"
)

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img = get_base64_image("cricket.jpg")

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpeg;base64,{img}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
[data-testid="stAppViewContainer"]::before {{
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(0, 0, 0, 0.45);
    z-index: 0;
}}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d47a1;
    color: #f0e6d3;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { display: none; }

.hero {
    text-align: center;
    padding: 3rem 0 2rem 0;
}

.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, #2d6a4f, #1b4332);
    border: 1px solid #40916c;
    color: #95d5b2;
    font-size: 0.7rem;
    font-family: 'DM Sans', sans-serif;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    padding: 0.4rem 1rem;
    border-radius: 2rem;
    margin-bottom: 1.5rem;
}

.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 4rem;
    font-weight: 900;
    line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 30%, #f9e04b 70%, #ffffff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 1rem 0;
}

.hero p {
    color: #ffffff;
    text-shadow: 1px 1px 4px rgba(0,0,0,0.9);
    font-size: 1.05rem;
    font-weight: 300;
    max-width: 400px;
    margin: 0 auto;
    line-height: 1.6;
}

.divider {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, #2d4a3e, transparent);
    margin: 2rem 0;
}

.chat-user {
    text-align: right;
    background: rgba(255,255,255,0.15);
    padding: 0.8rem 1rem;
    border-radius: 16px 16px 4px 16px;
    margin: 0.5rem 0;
    color: white;
    text-shadow: 1px 1px 4px rgba(0,0,0,0.9);
    font-size: 0.95rem;
}

.chat-bot {
    background: rgba(0,0,0,0.5);
    padding: 0.8rem 1rem;
    border-radius: 16px 16px 16px 4px;
    margin: 0.5rem 0;
    color: white;
    text-shadow: 1px 1px 4px rgba(0,0,0,0.9);
    font-size: 0.95rem;
    border-left: 3px solid #40916c;
}

footer {
    text-align: center;
    color: #ffffff;
    text-shadow: 1px 1px 4px rgba(0,0,0,0.9);
    font-size: 0.75rem;
    padding: 2rem 0;
    letter-spacing: 0.1em;
}

.stSpinner > div { border-top-color: #40916c !important; }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ RAG Powered</div>
    <h1>Cricket Agent</h1>
    <p>Ask anything about cricket — powered by AI</p>
</div>
<hr class="divider">
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<a href="/" target="_self"><button style="width:100%; padding:0.8rem; background:rgba(64,145,108,0.4); border:1px solid #40916c; border-radius:10px; color:white; font-size:1rem; cursor:pointer;">💬 AI Chat</button></a>', unsafe_allow_html=True)
with col2:
    st.markdown('<a href="/Dashboard" target="_self"><button style="width:100%; padding:0.8rem; background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2); border-radius:10px; color:white; font-size:1rem; cursor:pointer;">📊 Dashboard</button></a>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🏏 Cricket Agent")
    st.markdown("---")
    st.markdown("**How to use:**")
    st.markdown("1. Ask any cricket question!")
    st.markdown("2. Click 📝 to summarize all PDFs")
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("<small style='color:#3a4a5a'>Cricket Agent v2.0 RAG</small>", unsafe_allow_html=True)

api_key = st.secrets.get("GROQ_API_KEY", "")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# RAG functions
def split_into_chunks(text, chunk_size=500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

def find_relevant_chunks(question, chunks, top_k=5):
    if not chunks:
        return ""
    all_texts = [question] + chunks
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    question_vec = tfidf_matrix[0]
    chunk_vecs = tfidf_matrix[1:]
    similarities = cosine_similarity(question_vec, chunk_vecs)[0]
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    relevant = [chunks[i] for i in top_indices]
    return "\n\n".join(relevant)

# Auto-load PDFs
pdf_text = ""
page_count = 0
pdf_folder = "pdfs"
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

for filename in pdf_files:
    path = os.path.join(pdf_folder, filename)
    pdf = fitz.open(path)
    for page in pdf:
        pdf_text += page.get_text()
    page_count += len(pdf)

# Split into chunks for RAG
chunks = split_into_chunks(pdf_text)

if pdf_files:

    # Summary button
    if st.button("📝 Summarize All PDFs"):
        if not api_key:
            st.warning("⚠️ API key not found.")
        else:
            with st.spinner("Summarizing..."):
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{
                        "role": "user",
                        "content": f"You are a cricket expert. Summarize ALL these cricket documents in bullet points.\n\nDocuments:\n{pdf_text[:20000]}"
                    }]
                )
                summary = response.choices[0].message.content
            st.session_state.messages.append({"role": "user", "content": "📝 Summarize all PDFs"})
            st.session_state.messages.append({"role": "assistant", "content": summary})
            st.rerun()

    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bot">🏏 {msg["content"]}</div>', unsafe_allow_html=True)

    # Question input
    question = st.chat_input("Ask a question about cricket...")

    if question:
        if not api_key:
            st.warning("⚠️ API key not found.")
        else:
            st.session_state.messages.append({"role": "user", "content": question})

            with st.spinner("Analyzing..."):
                client = Groq(api_key=api_key)

                # Check if cricket related
                check_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{
                        "role": "user",
                        "content": f"Answer YES if the latest message is ANY of these: (1) related to cricket, (2) a greeting like hello/hi, (3) an emotion or appreciation like thank you/perfect/great/awesome/nice/wow/good, (4) a follow-up to previous cricket conversation, (5) a short response like ok/yes/no/sure. Answer NO only if it is clearly about a non-cricket topic like science, politics, food etc.\n\nPrevious messages: {[m['content'] for m in st.session_state.messages[-3:]]}\n\nLatest message: '{question}'"
                    }]
                )
                is_cricket = "YES" in check_response.choices[0].message.content.upper()

                if not is_cricket:
                    answer = "I only know about cricket! 🏏 Please ask me something about cricket players, matches, rules, tournaments, or history."
                else:
                    # RAG - find relevant chunks
                    relevant_context = find_relevant_chunks(question, chunks)

                    history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    history.insert(0, {
                        "role": "user",
                        "content": f"You are a cricket expert AI. Answer cricket questions directly from your knowledge. NEVER say 'the document does not mention'. Use the relevant context below for specific stats and facts. For future match predictions, always add a disclaimer that it is just a prediction and player availability may have changed.\n\nRelevant Context:\n{relevant_context}"
                    })
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=history
                    )
                    answer = response.choices[0].message.content

            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

else:
    st.markdown("""
    <div style="text-align:center; padding: 2rem; border: 1px dashed rgba(255,255,255,0.15); border-radius:16px;">
        <div style="font-size:3rem">🏏</div>
        <div style="font-size:0.9rem; margin-top:0.5rem; color:white;">No PDFs found in pdfs folder.</div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<hr class="divider">
<footer>CRICKET AGENT · RAG POWERED · 2026 · Built by Shashank DR</footer>
""", unsafe_allow_html=True)