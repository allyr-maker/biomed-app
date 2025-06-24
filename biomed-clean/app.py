import subprocess
import importlib.util

def install_model_if_needed():
    model_name = "en_core_sci_md"
    if importlib.util.find_spec(model_name) is None:
        print(f"{model_name} not found, installing...")
        subprocess.run([
            "pip", "install",
            "https://www.dropbox.com/scl/fo/hpvr9ko86pklswv7g33wi/ALLYSUgSzrVeO8K-4HbtWjE?rlkey=grf0qju29lfy3liww2igbkugu&st=f5774han&dl=0"
        ], check=True)
    else:
        print(f"{model_name} is already installed.")

install_model_if_needed()

# Now load the model
import spacy
nlp = spacy.load("en_core_sci_md")



import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from build_graph import build_entity_graph

import streamlit as st

st.set_page_config(page_title="BioMed Paper Analyzer", layout="wide")

st.title("🔬 Biomedical Paper Analyzer")
st.write("Upload a research paper and see gene/disease/pathway highlights.")

uploaded_file = st.file_uploader("Choose a research paper (.txt)")

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8", errors="ignore")
    st.subheader("📄 Extracted Text")
    st.text(text[:1000])  # Show first 1000 characters for preview
