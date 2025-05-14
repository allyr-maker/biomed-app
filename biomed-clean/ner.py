import spacy

# Load the SciSpaCy model with detailed biomedical entity types
try:
    nlp = spacy.load("en_ner_bionlp13cg_md")
except:
    raise RuntimeError("Model 'en_ner_bionlp13cg_md' not found. Install it with:\n"
                       "pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/"
                       "v0.2.4/en_ner_bionlp13cg_md-0.2.4.tar.gz")

def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent._.umls_ents if ent._.umls_ents else ent.label_) for ent in doc.ents]

# Optional test mode
if __name__ == "__main__":
    sample_text = "PI3K/AKT/mTOR inhibitors like everolimus show promise for glioblastoma treatment."
    doc = nlp(sample_text)

    print("🔬 Extracted Entities:")
    for ent in doc.ents:
        print(f"- {ent.text} [{ent.label_}]")
