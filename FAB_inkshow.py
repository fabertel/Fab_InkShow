from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse  # ✅ Import JSONResponse
import subprocess  # ✅ Import subprocess to run the script
import markdown
import os
import re
from fastapi import Request


app = FastAPI()

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

MARKDOWN_DIR = os.path.join(STATIC_DIR, "markdown")
script_path = os.path.join(os.path.dirname(__file__), "xls to json.py")
json_file_path = os.path.join(os.path.dirname(__file__), "static", "data.json")

SECRET_TOKEN = "jU5fXcOHrgjmtEZ4G8JaNJaf6Sd34tSFeiAZfYLFYuTI"  



# Serve static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Function to load Markdown
def load_markdown(filename):
    try:
        filepath = os.path.join(MARKDOWN_DIR, f"{filename}.md")
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Markdown file not found")
        with open(filepath, "r", encoding="utf-8") as f:
            return markdown.markdown(f.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading markdown: {str(e)}")


@app.get("/", response_class=HTMLResponse)
def home():
    with open(os.path.join(STATIC_DIR, "index.html"), "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.head("/")
async def head_root():
    return {}



# Route to serve dynamic markdown content in page.html


@app.get("/markdown/{page}", response_class=HTMLResponse)
def get_markdown(page: str, request: Request):
    if page == "admin":
        token = request.query_params.get("token")
        if token != SECRET_TOKEN:
            raise HTTPException(status_code=403, detail="Forbidden")
    return load_markdown(page)


@app.get("/videos", response_class=FileResponse)
async def videos_page():
    return FileResponse("static/videos.html", media_type="text/html")

def extract_date_key(filename):
    match = re.match(r'^(\d{6})', filename)
    return match.group(1) if match else "000000"  # fallback minimo






def extract_date_int(filename):
    match = re.search(r'(\d{6})', filename)
    return int(match.group(1)) if match else 0

@app.get("/api/videos")
async def list_videos():
    video_dir = "static/videos"
    files = os.listdir(video_dir)
    mp4_files = [f for f in files if f.lower().endswith(".mp4")]
    
    # Ordine alfabetico decrescente standard (dalla Z alla A)
    sorted_files = sorted(mp4_files, key=str.lower, reverse=True)
    
    print("🎞️ Sorted video list (standard descending alphabetical order):")
    for f in sorted_files:
        print(f" - {f}")
    
    return JSONResponse(sorted_files)

# Serve the generic page.html

@app.get("/page", response_class=HTMLResponse)
def get_page():
    with open(os.path.join(STATIC_DIR, "page.html"), "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/gallery/{gallery_id}", response_class=HTMLResponse)
def serve_gallery(gallery_id: str):
    with open(os.path.join(STATIC_DIR, "gallery.html"), "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())



@app.post("/regenerate-json")
async def regenerate_json():
    try:
        result = subprocess.run(["python", script_path], capture_output=True, text=True)
        if result.returncode == 0:
            return JSONResponse(content={"message": "✅ JSON successfully regenerated!"}, status_code=200)
        else:
            return JSONResponse(content={"message": f"❌ Error: {result.stderr}"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"message": f"❌ Exception: {str(e)}"}, status_code=500)
    


# ✅ Route to serve the latest JSON file
@app.get("/data.json")
async def get_json():
    return FileResponse(json_file_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
