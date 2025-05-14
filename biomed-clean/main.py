from summarizer import summarize_text
from ner import extract_entities
from build_graph import build_entity_graph

def main():
    # Example input: biomedical abstract or paragraph
    text = """
    Glioblastoma is an aggressive form of brain cancer with poor prognosis.
    Recent studies have focused on targeting the PI3K/AKT/mTOR pathway, which is
    frequently dysregulated in these tumors. Inhibitors such as everolimus and
    temsirolimus have shown promise in preclinical models. Additional mutations in
    TP53 and amplification of EGFR are also common in glioblastoma patients.
    """

    # Step 1: Summarize the text
    try:
        summary = summarize_text(text)
        print("📝 Summary:")
        print(summary)
    except Exception as e:
        print(f"❌ Error during summarization: {e}")
        summary = text  # fallback to original text

    # Step 2: Extract entities from the summary (or fallback text)
    try:
        entities = extract_entities(summary)
        print("\n🔍 Extracted Entities:")
        for ent in entities:
            print(f"{ent[0]} ({ent[1]})")
    except Exception as e:
        print(f"❌ Error during entity extraction: {e}")
        entities = []

    # Step 3: Build and display a knowledge graph
    if entities:
        try:
            build_entity_graph(entities)
        except Exception as e:
            print(f"❌ Error building graph: {e}")
    else:
        print("⚠️ No entities to build graph from.")

if __name__ == "__main__":
    main()

