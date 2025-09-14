from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import Any
from isclean import isclean
from isdent import isdent
import numpy as np
import  cv2
from fastapi.middleware.cors import CORSMiddleware

from PIL import Image
import io

app = FastAPI()




# Allow frontend (localhost:3000) to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy inference function (replace with your ML logic)
def inference(image_bytes: bytes) -> Any:



    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")  # already RGB

    is_clean = isclean(img)
    if 'error' in is_clean:
        return is_clean
    is_dent = isdent(img)

    return {
        "is_clean": is_clean["is_clean"],
        "is_clean_score": is_clean["is_clean_score"],
        "is_dent": is_dent["is_dent"],
        "is_dent_score": is_dent["is_dent_score"]
    }

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Read file as bytes
    image_bytes = await file.read()

    # Call your inference function
    result = inference(image_bytes)

    return JSONResponse(content=result)