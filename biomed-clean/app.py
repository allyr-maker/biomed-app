import os
import sys
import subprocess
import importlib.util
import streamlit as st
import streamlit.components.v1 as components

# ---- Disable Streamlit auto-reload (helps with repeated model installs) ----
os.environ["STREAMLIT_WATCHER_DISABLE_AUTO_RELOAD"] = "true"

# ---- Step 1: Ensure SciSpacy + small model is installed ----
def install_model_if_needed():
    # Install scispacy if missing
    if importlib.util.find_spec("scispacy") is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "scispacy==0.5.4"])

    # Install spaCy if missing
    if importlib.util.find_spec("spacy") is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "spacy==3.7.5"])

    # Install small SciSpacy model if missing
    try:
        import en_core_sci_sm
    except ImportError:
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            "https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_ner_bionlp13cg_md-0.5.4.tar.gz"
], check=True)