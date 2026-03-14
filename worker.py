import redis
import json
import fitz
from PIL import Image
from classifier import classify_document
from vector_store import store_document
from dotenv import load_dotenv

load_dotenv()

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def extract_text_from_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_image(file_path):
    img = Image.open(file_path)
    width, height = img.size
    mode = img.mode
    return f"image width:{width} height:{height} mode:{mode}"

def process_task(task):
    filename = task["filename"]
    file_path = task["file_path"]

    print(f"\n Processing: {filename}")

    if filename.lower().endswith(".pdf"):
        content = extract_text_from_pdf(file_path)
        file_type = "pdf"
    elif filename.lower().endswith((".jpg", ".jpeg", ".png")):
        content = extract_text_from_image(file_path)
        file_type = "image"
    else:
        content = "unknown file type"
        file_type = "unknown"

    # Classify karo
    category = classify_document(content)

    # Pinecone mein store karo
    store_document(filename, content, category)

    print(f" File: {filename}")
    print(f" Type: {file_type}")
    print(f" Category: {category}")
    print(f" Content preview: {content[:100]}")

    result = {
        "filename": filename,
        "file_type": file_type,
        "category": category,
        "status": "completed"
    }
    r.hset("results", filename, json.dumps(result))

def start_worker():
    print("Worker shuru ho gaya! Queue dekh raha hoon...")
    while True:
        task_data = r.brpop("task_queue", timeout=5)
        if task_data:
            _, task_json = task_data
            task = json.loads(task_json)
            process_task(task)
        else:
            print("Queue khaali hai, wait kar raha hoon...")

if __name__ == "__main__":
    start_worker()