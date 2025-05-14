from transformers import pipeline

print("⏳ Downloading model (this may take a few minutes)...")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
print("✅ Model loaded!")

text = """
Glioblastoma is an aggressive brain tumor with limited treatment options. Targeting the PI3K/AKT/mTOR pathway shows promise.
"""
summary = summarizer(text, max_length=30, min_length=10, do_sample=False)
print("📝 Summary:", summary[0]['summary_text'])
