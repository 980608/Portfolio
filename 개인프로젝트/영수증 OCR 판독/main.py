import sys
import os
sys.path.append(r"D:/AI_Coach/backend/app/")

from fastapi import FastAPI, UploadFile, File, HTTPException
import numpy as np
import cv2
import uuid
import asyncio

from db.db_data_save import get_conn
from receipt.receipt_service import process_receipt

app = FastAPI()


@app.post("/receipt/scan")
async def receipt_scan(file: UploadFile = File(...)):

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="이미지 파일만 가능")

    contents = await file.read()

    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        raise HTTPException(status_code=400, detail="이미지 로드 실패")

    task_id = str(uuid.uuid4())

    # DB INSERT
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO receipt (task_id, status)
        VALUES (%s, %s)
    """, (task_id, "processing"))

    conn.commit()
    cur.close()
    conn.close()

    # background task
    asyncio.create_task(
        asyncio.to_thread(process_receipt, task_id, img)
    )

    return {
        "task_id": task_id,
        "status": "processing"
    }
