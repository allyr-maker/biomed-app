from transformers import pipeline

# Initialize the summarization pipeline once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, max_length=130, min_length=30):
    """
    Summarizes the given text using a transformer model.
    
    Args:
        text (str): The text to summarize.
        max_length (int): Max summary length.
        min_length (int): Min summary length.

    Returns:
        str: A summarized version of the input text
"""
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']