import os
import logging 
<<<<<<< HEAD
from io import BytesIO
=======
from fastapi.responses import StreamingResponse

>>>>>>> 193f1b5 (Fix: Use StreamingResponse instead of Response)
from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from app.processing import process_image_bytes

ENVIRONMENT = os.getenv("ENV", "local")
API_SHARED_SECRET = os.getenv("API_SHARED_SECRET")

app = FastAPI(title="Image Processor API")

if ENVIRONMENT == "local":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

logger = logging.getLogger("image-processor") 
logger.setLevel(logging.INFO)

@app.post("/api/process")
async def process_image(
    image: UploadFile = File(...), 
    x_origin_verify: str = Header(...)
):
    logger.info(f"ENVIRONMENT={ENVIRONMENT}, API_SHARED_SECRET set={bool(API_SHARED_SECRET)}") 
    logger.info(f"Received header X-Origin-Verify={x_origin_verify}")
    
    if not API_SHARED_SECRET or x_origin_verify != API_SHARED_SECRET:
        logger.warning("Forbidden: header mismatch or secret not set")
        raise HTTPException(status_code=403, detail="Forbidden")
        
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image type")
    
    image_bytes = await image.read()
    logger.info(f"Received image size: {len(image_bytes)} bytes")
    
    try:
        result_bytes = process_image_bytes(image_bytes)
        logger.info(f"Processed image size: {len(result_bytes)} bytes")
        
        if not result_bytes or len(result_bytes) == 0:
            raise ValueError("Processed image is empty")
            
    except Exception as e:
        logger.exception("Error processing image") 
        raise HTTPException(status_code=500, detail=str(e))
    
    return StreamingResponse(
        BytesIO(result_bytes),
        media_type="image/jpeg",
        headers={"Content-Length": str(len(result_bytes))}
    )
