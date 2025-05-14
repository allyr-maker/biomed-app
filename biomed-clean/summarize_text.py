from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# Load the summarization pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Load BioBERT model for NER
tokenizer = AutoTokenizer.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
model = AutoModelForTokenClassification.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
ner = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# Read the abstracts file
with open("abstracts.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Break the text into chunks for processing
MAX_CHARS = 1000
chunks = [text[i:i + MAX_CHARS] for i in range(0, len(text), MAX_CHARS)]

# Open the output file to write summaries and entities
with open("output.txt", "w", encoding="utf-8") as output_file:
    # Loop through the chunks
    for i, chunk in enumerate(chunks):
        # Summarize each chunk
        summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]
        
        # Write summary to file
        output_file.write(f"--- SUMMARY for Chunk {i + 1} ---\n")
        output_file.write(summary + "\n\n")
        
        # Extract entities from the chunk
        entities = ner(chunk)
        output_file.write(f"--- ENTITIES for Chunk {i + 1} ---\n")
        
        # Write entities to file
        for ent in entities:
            output_file.write(f"{ent['word']} ({ent['entity_group']}) - Confidence: {ent['score']:.2f}\n")
        
        # Add a separator between chunks
        output_file.write("\n" + "-" * 40 + "\n\n")

print("Summaries and entities have been saved to output.txt")


from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# Load BioBERT model for NER (Biomedical Named Entity Recognition)
tokenizer = AutoTokenizer.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
model = AutoModelForTokenClassification.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
ner = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# Loop through the summarized chunks and extract entities
print("\n--- ENTITY EXTRACTION ---")
for chunk in chunks:
    entities = ner(chunk)
    print(f"\nEntities in chunk:")
    for ent in entities:
        print(f"{ent['word']} ({ent['entity_group']}) - confidence: {ent['score']:.2f}")
    print("-" * 40)
