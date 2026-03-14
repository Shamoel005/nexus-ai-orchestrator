import redis
import json
import fitz
from PIL import Image
from classifier import classify_document
from vector_store import store_document
from dotenv import load_dotenv
import os

load_dotenv()

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def extract_text_from_pdf(file_path):
    try:
        text = ""
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        if not text.strip():
            return "empty pdf no text found"
        return text
    except Exception as e:
        print(f" PDF read nahi hua: {e}")
        return "pdf read error"

def extract_text_from_image(file_path):
    try:
        img = Image.open(file_path)
        width, height = img.size
        mode = img.mode
        return f"image width:{width} height:{height} mode:{mode}"
    except Exception as e:
        print(f" Image read nahi hui: {e}")
        return "image read error"

def process_task(task):
    try:
        filename = task["filename"]
        file_path = task["file_path"]

        print(f"\n Processing: {filename}")

        # File exist karti hai?
        if not os.path.exists(file_path):
            print(f" File nahi mili: {file_path}")
            return

        # File type check karo
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

        # Result Redis mein store karo
        result = {
            "filename": filename,
            "file_type": file_type,
            "category": category,
            "status": "completed"
        }
        r.hset("results", filename, json.dumps(result))

    except Exception as e:
        print(f" Error processing task: {e}")
        # Failed task ko bhi store karo
        result = {
            "filename": task.get("filename", "unknown"),
            "status": "failed",
            "error": str(e)
        }
        r.hset("results", task.get("filename", "unknown"), json.dumps(result))

def start_worker():
    print("Worker shuru ho gaya! Queue dekh raha hoon...")
    while True:
        try:
            task_data = r.brpop("task_queue", timeout=5)
            if task_data:
                _, task_json = task_data
                task = json.loads(task_json)
                process_task(task)
            else:
                print("Queue khaali hai, wait kar raha hoon...")
        except redis.ConnectionError:
            print(" Redis connection toot gayi! 3 second mein retry...")
            import time
            time.sleep(3)
        except Exception as e:
            print(f" Worker error: {e}")

if __name__ == "__main__":
    start_worker()