from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter(prefix="/upload", tags=["upload"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    # 1. Kiểm tra định dạng file
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, detail="Only PDF files are allowed."
        )

    # 2. Tạo tên file ngẫu nhiên tránh trùng lặp
    filename = f"{uuid4()}.pdf"
    file_path = UPLOAD_DIR / filename

    # 3. Ghi file vào thư mục lưu trữ
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 4. Trả về kết quả cho client
    return {
        "message": "PDF uploaded successfully.",
        "filename": file.filename,
        "path": str(file_path),
    }