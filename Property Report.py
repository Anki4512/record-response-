import os
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaLLM
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
# (Keep your existing LangChain imports here)

st.set_page_config(page_title="Hollywood Property Assistant", page_icon="🏛️")
st.title("Hollywood, FL Property Assistant 🏛️")

# We use this to keep the chat history visible in the browser
if "messages" not in st.session_state:
    st.session_state.messages = []

# 1. ROBUST LOADING & METADATA TAGGING
print("--- Loading & Tagging Documents ---")
loader = DirectoryLoader('.', glob="./*.pdf", loader_cls=PyMuPDFLoader)
all_documents = loader.load()

category_map = {
    "zoning.pdf": "Policy",
    "preservation.pdf": "Historic",
    "hollywood-fl-1.pdf": "Legal Code",
    "Future land use.pdf": "Planning",
    "Neighborhood plan.pdf": "Planning",
    "Residential construction.pdf": "Permits"
}

for doc in all_documents:
    file_name = os.path.basename(doc.metadata.get('source', ''))
    doc.metadata['category'] = category_map.get(file_name, "General")

# 2. SMART CHUNKING
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
texts = text_splitter.split_documents(all_documents)

# 3. VECTOR STORAGE
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = Chroma.from_documents(texts, embeddings, persist_directory="./hollywood_db")
def get_metadata_filter(question):
    question = question.lower()
    
    # Check for keywords and return the matching category
    if "historic" in question or "preservation" in question:
        return {"category": "Historic"}
    elif "permit" in question or "application" in question:
        return {"category": "Permits"}
    elif "land use" in question or "zoning" in question:
        return {"category": "Zoning"}
    elif "neighborhood" in question or "vision" in question:
        return {"category": "Planning"}
    
    # If no keywords match, return None to search everything
    return None

# 📍 UPGRADE 1: SOURCE ATTRIBUTION
# This function formats documents so the AI sees the source and page number
def format_docs_with_sources(docs):
    formatted = []
    for doc in docs:
        source = os.path.basename(doc.metadata.get('source', 'Unknown'))
        page = doc.metadata.get('page', 0) + 1  # Standardizing to 1-based index
        formatted.append(f"--- SOURCE: {source} (Page {page}) ---\n{doc.page_content}")
    return "\n\n".join(formatted)

# 🔍 UPGRADE 2: INTELLIGENT FILTERING
# We define a retriever that can be configured with filters later if needed
retriever = vector_db.as_retriever(search_kwargs={"k": 5})

# ⚖️ UPGRADE 3: CHECK-STEP TEMPLATE
# The prompt now forces the AI to use sources and grade its own confidence
template = """You are a professional City Planning Assistant for Hollywood, FL.
Use the following pieces of context to answer the question. 
ALWAYS cite the Source and Page number for each fact you provide.

At the end of your answer, provide a 'CONFIDENCE GRADE' (A, B, or C):
- A: Answer is fully supported by the text.
- B: Answer is partially supported, but some details are missing.
- C: Context does not provide a direct answer.

{context}

Question: {question}
Answer:"""

prompt = ChatPromptTemplate.from_template(template)
llm = OllamaLLM(model="llama3")

# CHAIN CONSTRUCTION
rag_chain = (
    {"context": retriever | format_docs_with_sources, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# EXECUTION
query = "what are the zoning restrictions for residential construction in Hollywood, FL?"
print("\n--- GENERATING VERIFIABLE REPORT ---")
print(rag_chain.invoke(query))