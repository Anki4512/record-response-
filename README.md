https://github.com/Anki4512/record-response-/blob/main/Gemini_Generated_Image_lrpjpllrpjpllrpj.png
🏛️ Hollywood, FL Property & Planning Assistant
Official Executive AI Portal | Office of the Mayor

This project is an AI-powered Retrieval-Augmented Generation (RAG) system built to assist city officials and residents in navigating Hollywood, Florida's complex zoning codes, historic preservation guidelines, and residential construction permits.

🚀 System Architecture & Workflow
The assistant uses a "Search-then-Verify" logic to ensure every answer is grounded in official city documentation.

Code snippet
graph TD
    A[User Question] --> B{Keyword Router}
    B -- "Historic" --> C[Filter: Preservation.pdf]
    B -- "Zoning" --> D[Filter: Zoning.pdf]
    B -- "General" --> E[Search All Docs]
    
    C & D & E --> F[ChromaDB Vector Retrieval]
    F --> G[Context Augmentation]
    G --> H[Llama 3 LLM via Ollama]
    H --> I[Response with Citations]
    I --> J[Confidence Grade: A/B/C]
✨ Premium Features
Executive UI: A high-end Streamlit interface featuring City of Hollywood branding, Mayor Josh Levy's welcome, and a "Classic Institutional" design.

Source Attribution: Every response includes the specific PDF filename and Page Number for legal verification.

Intelligent Metadata Routing: Automatically filters searches based on keywords like "zoning," "historic," or "permits" to increase accuracy.

Motion Animations: Custom CSS transitions providing a modern, fluid user experience.

High-Capacity Contrast: Optimized typography for maximum readability against architectural backgrounds.

🛠️ Technical Stack
Interface: Streamlit

Orchestration: LangChain

Brain (LLM): Ollama (Llama 3)

Vector Database: ChromaDB

Embeddings: HuggingFace all-MiniLM-L6-v2

Data Processing: PyMuPDF & Recursive Character Splitting

⚙️ Installation & Setup
1. Prerequisites

Python 3.10+

Ollama installed and running (ollama run llama3)

2. Clone and Environment Setup

Bash
git clone https://github.com/your-username/hollywood-property-assistant.git
cd hollywood-property-assistant
source gis_env/bin/activate
3. Install Dependencies

Bash
pip install streamlit langchain chromadb langchain-community langchain-huggingface langchain-ollama pymupdf
4. Run the Application

Bash
python -m streamlit run streamlit_app.py
📁 Project Directory
streamlit_app.py: The main frontend with Executive CSS and branding.

Property_Report.py: The backend logic for document loading and RAG chain construction.

hollywood_db/: Local storage for the vectorized city documents.

*.pdf: Source documentation (Zoning, Neighborhood Plans, etc.).

⚖️ Disclaimer
This tool is an AI assistant intended for informational purposes and should not replace professional legal or urban planning advice from the City of Hollywood departments.
