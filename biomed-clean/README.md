# Biomedical Paper Analyzer

This Streamlit app allows users to upload biomedical research papers (as `.txt` files) and visualize links between genes, diseases, and pathways using a knowledge graph.

---

## Features

- Upload a research paper in plain text format.
- Extract and preview text from the uploaded paper.
- Automatically identify biomedical entities using NLP.
- Build and display an interactive entity graph.

---

## How to Use (Deployed Version)

1. Visit the app on Streamlit Cloud.
2. Upload a `.txt` research paper using the file uploader.
3. Preview the extracted text.
4. View the generated entity graph in the embedded viewer.

**Note:** On free-tier deployments, the app uses a smaller NLP model (`en_core_sci_sm`) to ensure fast startup and low memory usage. This may result in slightly fewer recognized entities.

---

## Local Setup (Optional / Advanced)

1. Clone the repository:

   ```bash
   git clone <your-repo-url>
   cd biomed-app
