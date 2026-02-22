import streamlit as st
import os
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaLLM
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
# Updated CSS for Classic Institutional Look
# Update your CSS block with this background logic
import streamlit as st
import base64
import os

# --- 1. HELPER FUNCTION TO ENCODE LOCAL IMAGE ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- 2. SET THE BACKGROUND IMAGE PATH ---
# Using the path you provided
img_path = "/Users/ankireddy/Desktop/Record_response/VAYm4w.png"
img_base64 = get_base64_of_bin_file(img_path)

# --- 3. APPLY PREMIUM CSS WITH LOCAL BACKGROUND ---
st.markdown(f"""
    <style>
    @import url('/Users/ankireddy/Desktop/Record_response/VAYm4w.png');
    .stApp {{
        background: linear-gradient(
            rgba(0, 0, 0, 0.4), /* Adding a slight dark tint helps white text pop */
            rgba(0, 0, 0, 0.4)
        ), 
        url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* Change all main titles and text to White */
    h1, h2, h3, p, span, label {{
        color: #FFFFFF !important;
        font-family: 'Playfair Display', serif !important;
        /* A subtle shadow makes white text readable on any image */
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }}

    /* Customizing the Subheader (Mayor's Title) */
    .mayor-text {{
        color: #FFFFFF !important;
        opacity: 0.9;
        font-style: italic;
    }}

    /* Keep the Chat Bubbles readable with dark text on white background */
    .stChatMessage p {{
        color: #333333 !important;
        text-shadow: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 2. Executive Branding Layout
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    # Official City Seal (Placeholder URL - replace with actual link)
    st.image("/Users/ankireddy/Desktop/Record_response/channels4_profile.jpg", width=120)

with col2:
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.header("Office of the Mayor")
    st.subheader("Property & Planning Assistant")
    st.markdown('<p class="mayor-text">"Welcome to the official Property Assistant portal."</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    # Mayor Josh Levy Portrait (Placeholder URL)
    st.image("/Users/ankireddy/Desktop/Record_response/channels4_profile.jpg", width=120)

# --- PAGE SETUP ---
st.set_page_config(page_title="Hollywood AI Assistant", page_icon="🏛️")
st.title("Hollywood, FL Property Assistant 🏛️")

# --- CACHED DATA LOADING ---
@st.cache_resource
def load_rag_system():
    # Load and Tag
    loader = DirectoryLoader('.', glob="./*.pdf", loader_cls=PyMuPDFLoader)
    docs = loader.load()
    
    # We use your category mapping here
    category_map = {
        "zoning.pdf": "Zoning",
        "preservation.pdf": "Historic",
        "hollywood-fl-1.pdf": "Legal Code",
        "Future land use.pdf": "Planning",
        "Neighborhood plan.pdf": "Planning",
        "Residential construction.pdf": "Permits"
    }
    for d in docs:
        fname = os.path.basename(d.metadata.get('source', ''))
        d.metadata['category'] = category_map.get(fname, "General")

    # Split
    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
    texts = splitter.split_documents(docs)

    # Index
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma.from_documents(texts, embeddings, persist_directory="./hollywood_db")
    
    # Chain
    llm = OllamaLLM(model="llama3")
    template = """Use the context to answer. Always cite Source and Page.
    {context}
    Question: {question}
    Answer:"""
    prompt = ChatPromptTemplate.from_template(template)
    
    def format_docs(docs):
        return "\n\n".join(f"SOURCE: {os.path.basename(d.metadata['source'])} (P.{d.metadata.get('page',0)+1})\n{d.page_content}" for d in docs)

    return (
        {"context": vector_db.as_retriever() | format_docs, "question": RunnablePassthrough()}
        | prompt | llm | StrOutputParser()
    )

# Start the "Engine"
with st.spinner("🤖 Waking up the AI and reading PDFs..."):
    rag_chain = load_rag_system()

# --- CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- USER INPUT ---
if user_input := st.chat_input("Ask me about Hollywood zoning or permits..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents..."):
            response = rag_chain.invoke(user_input)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})