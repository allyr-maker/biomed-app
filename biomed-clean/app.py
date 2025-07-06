import subprocess
import importlib.util

def install_model_if_needed():
    import subprocess
    import importlib.util

    if importlib.util.find_spec("en_ner_bionlp13cg_md") is None:
        subprocess.run([
           "pip",
            "install",
             "https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_ner_bionlp13cg_md-0.5.4.tar.gz"
        ], check=True)
    else:
       print("en_ner_bionlp13cg_md is already installed.")

install_model_if_needed()

# Now load the model
import spacy
nlp = spacy.load("en_ner_bionlp13cg_md")



import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from build_graph import build_entity_graph
with open("biomed-clean/entity_graph.html", "r", encoding="utf-8") as f:
    html_code = f.read()
st.components.v1.html(html_code, height=800, scrolling=True)

import streamlit as st

st.set_page_config(page_title="BioMed Paper Analyzer", layout="wide")

st.title("🔬 Biomedical Paper Analyzer")
st.write("Upload a research paper and see gene/disease/pathway highlights.")

uploaded_file = st.file_uploader("Choose a research paper (.txt)")

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8", errors="ignore")
    st.subheader("📄 Extracted Text")
    st.text(text[:1000])  # Show first 1000 characters for preview
