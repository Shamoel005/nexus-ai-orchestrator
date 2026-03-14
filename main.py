from fastapi import FastAPI, UploadFile, File
import shutil
import os
import redis
import json

app = FastAPI()

# Redis se connect karo
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

UPLOAD_FOLDER = "uploads"

# Uploads folder banao agar nahi hai toh
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {"message": "Nexus API chal raha hai!"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    
    # File save karo uploads folder mein
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Redis queue mein daalo
    task = {
        "filename": file.filename,
        "file_path": file_path
    }
    r.lpush("task_queue", json.dumps(task))
    
    return {
        "message": "File upload ho gayi!",
        "filename": file.filename,
        "status": "Queue mein daal diya"
    }

@app.get("/status")
def get_status():
    queue_length = r.llen("task_queue")
    return {
        "queue_mein_pending": queue_length
    }
@app.get("/results")
def get_results():
    all_results = r.hgetall("results")
    parsed = {}
    for filename, data in all_results.items():
        parsed[filename] = json.loads(data)
    return parsed
@app.get("/search")
async def search_documents(query: str):
    from vector_store import search_similar
    
    if not query:
        return {"error": "Query dalo bhai!"}
    
    results = search_similar(query)
    
    if not results:
        return {"message": "Koi similar document nahi mila", "results": []}
    
    formatted = []
    for match in results:
        formatted.append({
            "filename": match.metadata.get("filename"),
            "category": match.metadata.get("category"),
            "similarity_score": round(match.score, 3),
            "preview": match.metadata.get("preview", "")[:100]
        })
    
    return {
        "query": query,
        "results": formatted
    }