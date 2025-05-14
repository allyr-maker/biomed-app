# pipeline.py
from summarizer import summarize_text
from ner import extract_entities

def process_text(text):
    summary = summarize_text(text)
    print("\n📝 Summary:")
    print(summary)

    entities = extract_entities(summary)
    print("\n🔬 Extracted Entities:")
    for ent_text, ent_label in entities:
        print(f"- {ent_text} [{ent_label}]")

if __name__ == "__main__":
    input_text = """
    Glioblastoma is one of the most aggressive forms of brain cancer. PI3K/AKT/mTOR inhibitors,
    such as everolimus, have shown promise in treating glioblastoma by targeting tumor growth pathways.
    However, resistance mechanisms and adverse effects remain challenges for clinical applications.
    """
    process_text(input_text)
