import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncpg
from datetime import datetime
from typing import List

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/postgres')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.create_pool(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.presentationml.presentation", "text/plain"]:
        raise HTTPException(status_code=400, detail="Unsupported file type.")
    query = """
        INSERT INTO uploaded_files (filename, content_type, file_data)
        VALUES ($1, $2, $3)
        RETURNING id, filename, content_type, uploaded_at
    """
    async with app.state.db.acquire() as conn:
        row = await conn.fetchrow(query, file.filename, file.content_type, content)
    return {"id": row["id"], "filename": row["filename"], "content_type": row["content_type"], "uploaded_at": row["uploaded_at"]}

@app.get("/files")
async def list_files():
    query = "SELECT id, filename, content_type, uploaded_at FROM uploaded_files ORDER BY uploaded_at DESC"
    async with app.state.db.acquire() as conn:
        rows = await conn.fetch(query)
    return [{"id": r["id"], "filename": r["filename"], "content_type": r["content_type"], "uploaded_at": r["uploaded_at"]} for r in rows]

@app.get("/files/{file_id}")
async def download_file(file_id: int):
    query = "SELECT filename, content_type, file_data FROM uploaded_files WHERE id=$1"
    async with app.state.db.acquire() as conn:
        row = await conn.fetchrow(query, file_id)
    if not row:
        raise HTTPException(status_code=404, detail="File not found.")
    return StreamingResponse(
        iter([row["file_data"]]),
        media_type=row["content_type"],
        headers={"Content-Disposition": f"attachment; filename={row['filename']}"}
    ) 