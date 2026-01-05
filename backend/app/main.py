import os
import logging 

from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

from app.processing import process_image_bytes

# Default to local if not set
ENVIRONMENT = os.getenv("ENV", "local")
API_SHARED_SECRET = os.getenv("API_SHARED_SECRET")

app = FastAPI(title="Image Processor API")


# CORS ONLY FOR LOCAL DEVELOPMENT
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
@app.post("/process")
async def process_image( image: UploadFile = File(...), x_origin_verify: str = Header(...)):
    logger.info(f"ENVIRONMENT={ENVIRONMENT}, API_SHARED_SECRET set={bool(API_SHARED_SECRET)}") 
    logger.info(f"Received header X-Origin-Verify={x_origin_verify}")

    if not API_SHARED_SECRET or x_origin_verify != API_SHARED_SECRET:
        logger.warning("Forbidden: header mismatch or secret not set")
        raise HTTPException(status_code=403, detail="Forbidden")
        

    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image type")



    image_bytes = await image.read()

    try:
        result_bytes = process_image_bytes(image_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return Response(
        content=result_bytes,
        media_type="image/jpeg",
    )
