from fastapi import FastAPI, UploadFile, File, HTTPException
import requests
import numpy as np
from PIL import Image

app = FastAPI()

# Vertex endpoint URL (replace this with your real endpoint URL later)
VERTEX_ENDPOINT_URL = "https://your-endpoint-url-here/predict"

# Size your model expects
IMG_SIZE = (224, 224)

def preprocess_image(file: UploadFile) -> np.ndarray:
    img = Image.open(file.file).convert('RGB')
    img = img.resize(IMG_SIZE)
    arr = np.array(img) / 255.0  # Normalize
    arr = arr.astype(np.float32)  # Ensure type
    return arr

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        img_array = preprocess_image(file)
        payload = {"instances": [img_array.tolist()]}

        response = requests.post(VERTEX_ENDPOINT_URL, json=payload)
        response.raise_for_status()

        predictions = response.json().get("predictions", [])
        return {"predictions": predictions}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}
