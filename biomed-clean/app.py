import subprocess
import importlib.util
import sys
import os
import streamlit as st
import streamlit.components.v1 as components

# 1. Ensure the model is installed
def install_model_if_needed():
    if importlib.util.find_spec("en_ner_bionlp13cg_md") is None:
        subprocess.run([
            "pip",
            "install",
            "https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_ner_bionlp13cg_md-0.5.4.tar.gz"
        ], check=True)
    else:
        print("en_ner_bionlp13cg_md is already installed.")

install_model_if_needed()

# 2. Load the model
import spacy
nlp = spacy.load("en_ner_bionlp13cg_md")

# 3. Setup sys.path and import build_graph
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from build_graph import build_entity_graph

# 4. Set Streamlit page config and UI
st.set_page_config(page_title="BioMed Paper Analyzer", layout="wide")
st.title("🔬 Biomedical Paper Analyzer")
st.write("Upload a research paper and see gene/disease/pathway highlights.")

uploaded_file = st.file_uploader("Choose a research paper (.txt)")

# 5. Only build and load the graph if the file exists or was uploaded
if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8", errors="ignore")
    st.subheader("📄 Extracted Text")
    st.text(text[:1000])  # Show preview

    # You probably want to run your full pipeline here (summarize, extract entities, etc.)
    # Then build the graph from that output:
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(text)
    build_entity_graph()

    # Load and display the generated graph
    html_path = os.path.join("biomed-clean", "entity_graph.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html_code = f.read()
        components.html(html_code, height=800, scrolling=True)
    else:
        st.error("⚠️ entity_graph.html not found after building the graph.")
