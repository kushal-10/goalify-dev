
# Function to split text into chunks
def split_text_into_chunks(text, chunk_size=200, overlap=20):
    words = text.split()  # Split text into words
    chunks = []
    
    i = 0
    while i < len(words):
        chunk = words[i:i + chunk_size]  # Take 200 words
        chunks.append(" ".join(chunk))  # Convert list back to string
        i += chunk_size - overlap  # Move ahead with overlap
    
    return chunks
