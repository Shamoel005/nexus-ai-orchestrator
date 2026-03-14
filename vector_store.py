from pinecone import Pinecone
from dotenv import load_dotenv
import os
import hashlib
import numpy as np

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

def text_to_vector(text, size=384):
    """Text ko simple vector mein badlo — no internet needed!"""
    text = text[:500].lower()
    vector = np.zeros(size)
    
    for i, char in enumerate(text):
        pos = (ord(char) * (i + 1)) % size
        vector[pos] += 1
    
    # Normalize karo
    norm = np.linalg.norm(vector)
    if norm > 0:
        vector = vector / norm
    
    return vector.tolist()

def store_document(filename, text, category):
    """Document ko vector mein badlo aur Pinecone mein store karo"""
    vector = text_to_vector(text)
    
    index.upsert(vectors=[{
        "id": filename,
        "values": vector,
        "metadata": {
            "filename": filename,
            "category": category,
            "preview": text[:200]
        }
    }])
    
    print(f" Pinecone mein store ho gaya: {filename}")

def search_similar(text, top_k=3):
    """Similar documents dhundho"""
    vector = text_to_vector(text)
    
    results = index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True
    )
    
    return results.matches