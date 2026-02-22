import streamlit as st
import ollama
from pypdf import PdfReader
import os

# Set up the Web Page Title and Icon
st.set_page_config(page_title="Hollywood FL Zoning Bot", page_icon="🌴")

st.title("🌴 City of Hollywood Planning Assistant")
st.markdown("### AI-Powered Zoning & Comprehensive Plan Search")

# Configuration
PDF_FILE_PATH = "/Users/ankireddy/Desktop/Record_response/zoning.pdf"

def get_pdf_context(path):
    if not os.path.exists(path):
        return None
    reader = PdfReader(path)
    text = ""
    # Reading first 15 pages for context
    for i in range(min(15, len(reader.pages))):
        text += f"\n--- PAGE {i+1} ---\n" + reader.pages[i].extract_text()
    return text

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask a question about Hollywood's Land Use or Zoning..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching the Comprehensive Plan..."):
            context = get_pdf_context(PDF_FILE_PATH)
            
            if context:
                full_prompt = f"""
                You are a professional City Planning Assistant for Hollywood, FL.
                Use the following text to answer. Cite page numbers.
                Context: {context}
                User Question: {prompt}
                """
                
                response = ollama.chat(model='llama3', messages=[
                    {'role': 'user', 'content': full_prompt},
                ])
                
                answer = response['message']['content']
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error("Error: 'zoning.pdf' not found in the directory.")