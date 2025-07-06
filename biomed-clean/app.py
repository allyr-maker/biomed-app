import os
import sys
import subprocess
import importlib.util
import streamlit as st
import streamlit.components.v1 as components

# ---- Step 1: Ensure NER model is installed ----
def install_model_if_needed():
    if importlib.util.find_spec("en_ner_bionlp13cg_md") is None:
        subprocess.run([
            "pip",
            "install",
            "https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_ner_bionlp13cg_md-0.5.4.tar.gz"
        ], check=True)

install_model_if_needed()

# ---- Step 2: Load spaCy model ----
import spacy
nlp = spacy.load("en_ner_bionlp13cg_md")

# ---- Step 3: Adjust Python path and import graph logic ----
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from build_graph import build_entity_graph

# ---- Step 4: Streamlit UI Setup ----
st.set_page_config(page_title="BioMed Paper Analyzer", layout="wide")
st.title("🔬 Biomedical Paper Analyzer")
st.write("Upload a research paper and visualize gene/disease/pathway links.")

uploaded_file = st.file_uploader("Choose a research paper (.txt)")

# ---- Step 5: Handle uploaded file ----
if uploaded_file is not None:
    # Read and save file
    text = uploaded_file.read().decode("utf-8", errors="ignore")

    output_path = os.path.join("biomed-clean", "output.txt")
    os.makedirs("biomed-clean", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    st.subheader("📄 Extracted Text Preview")
    st.text(text[:1000])  # Show preview

    # ---- Step 6: Build graph ----
    try:
        build_entity_graph()
    except Exception as e:
        st.error(f"❌ Failed to build graph: {e}")
    
    # ---- Step 7: Display graph ----
    html_path = os.path.join("biomed-clean", "entity_graph.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html_code = f.read()
        components.html(html_code, height=800, scrolling=True)
    else:
        st.warning("⚠️ entity_graph.html not found.")
