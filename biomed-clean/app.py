import os
import sys
import streamlit as st
import streamlit.components.v1 as components
import spacy

# Disable auto-reload for stability
os.environ["STREAMLIT_WATCHER_DISABLE_AUTO_RELOAD"] = "true"

# ---- Step 0: Determine environment ----
STREAMLIT_ENV = os.getenv("STREAMLIT_ENV", "local")  # Set STREAMLIT_ENV=free on Streamlit Cloud

# ---- Step 1: Load spaCy model ----
def load_model(lazy=False):
    """Load appropriate spaCy model depending on environment."""
    if STREAMLIT_ENV == "free":
        model_name = "en_core_sci_sm"
        st.info("Using lightweight model for free deployment.")
        return spacy.load(model_name)
    
    # Local/high-RAM environment
    if lazy:
        # Lazy-load large model only on button click
        return None
    else:
        try:
            model_name = "en_ner_bionlp13cg_md"
            st.info("Using full SciSpacy model (high-accuracy).")
            return spacy.load(model_name)
        except OSError as e:
            st.warning(f"Could not load {model_name}: {e}")
            st.info("Falling back to small model en_core_sci_sm")
            return spacy.load("en_core_sci_sm")

# ---- Step 2: Streamlit UI Setup ----
st.set_page_config(page_title="BioMed Paper Analyzer", layout="wide")
st.title("🔬 Biomedical Paper Analyzer")
st.write("Upload a research paper and visualize gene/disease/pathway links.")

uploaded_file = st.file_uploader("Choose a research paper (.txt)")

# ---- Step 3: Lazy-load button for full model ----
nlp = load_model(lazy=True)
if STREAMLIT_ENV != "free" and nlp is None:
    if st.button("Load full NER model (large)"):
        nlp = load_model(lazy=False)
        st.success("Full model loaded!")

# ---- Step 4: Handle uploaded file ----
if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8", errors="ignore")
    
    output_path = os.path.join("biomed-clean", "output.txt")
    os.makedirs("biomed-clean", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    
    st.subheader("📄 Extracted Text Preview")
    st.text(text[:1000])
    
    # ---- Step 5: Only build graph if model is loaded ----
    if nlp is None:
        st.warning("⚠️ NER model not loaded. Click 'Load full NER model' to proceed.")
    else:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from build_graph import build_entity_graph
        
        try:
            build_entity_graph()
        except Exception as e:
            st.error(f"❌ Failed to build graph: {e}")
        
        html_path = os.path.join("biomed-clean", "entity_graph.html")
        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8") as f:
                html_code = f.read()
            components.html(html_code, height=800, scrolling=True)
        else:
            st.warning("⚠️ entity_graph.html not found.")
