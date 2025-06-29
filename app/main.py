from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from app.clothing_seg import segment_bytes
import os

app = FastAPI(title="Clothing Segmentation (full mask)")

@app.post("/segment")
async def segment(file: UploadFile = File(...)):
    if not file.content_type.startswith("image"):
        raise HTTPException(415, "File must be an image")

    raw = await file.read()
    mask_path, parts = segment_bytes(raw)

    return JSONResponse({
        "mask_png": os.path.basename(mask_path),
        "parts": {k: os.path.basename(v) for k, v in parts.items()}
    })

@app.get("/download/{filename}")
async def download(filename: str):
    return FileResponse(f"/tmp/{filename}")
