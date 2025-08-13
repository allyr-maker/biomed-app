import os
import sys
import streamlit as st
import streamlit.components.v1 as components
import spacy

# ---- Disable Streamlit auto-reload (optional) ----
os.environ["STREAMLIT_WATCHER_DISABLE_AUTO_RELOAD"] = "true"

# ---- Load small SciSpacy model ----
try:
    nlp = spacy.load("en_core_sci_sm")
except OSError:
    st.error(
        "SciSpacy small model 'en_core_sci_sm' not found. "
        "Make sure you installed dependencies from requirements.txt."
    )
    st.stop()

# ---- Adjust Python path for graph code ----
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from build_graph import build_entity_graph

# ---- Streamlit UI ----
st.set_page_config(page_title="BioMed Paper Analyzer", layout="wide")
st.title("🔬 Biomedical Paper Analyzer")
st.write("Upload a research paper and visualize gene/disease/pathway links.")

uploaded_file = st.file_uploader("Choose a research paper (.txt)")

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8", errors="ignore")

    output_path = os.path.join("biomed-clean", "output.txt")
    os.makedirs("biomed-clean", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    st.subheader("📄 Extracted Text Preview")
    st.text(text[:1000])

    # ---- Build graph ----
    try:
        build_entity_graph()
    except Exception as e:
        st.error(f"❌ Failed to build graph: {e}")

    # ---- Display graph ----
    html_path = os.path.join("biomed-clean", "entity_graph.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html_code = f.read()
        components.html(html_code, height=800, scrolling=True)
    else:
        st.warning("⚠️ entity_graph.html not found.")
