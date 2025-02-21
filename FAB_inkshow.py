from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse  # ✅ Import JSONResponse
import subprocess  # ✅ Import subprocess to run the script
import markdown
import os

app = FastAPI()

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
MARKDOWN_DIR = os.path.join(STATIC_DIR, "markdown")
script_path = os.path.join(os.path.dirname(__file__), "xls to json.py")
json_file_path = os.path.join(os.path.dirname(__file__), "static", "data.json")


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
def get_markdown(page: str):
    return load_markdown(page)

# Serve the generic page.html
@app.get("/page", response_class=HTMLResponse)
def get_page():
    with open(os.path.join(STATIC_DIR, "page.html"), "r", encoding="utf-8") as f:
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
