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
