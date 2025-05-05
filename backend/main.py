from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import io
import base64
import numpy as np
from PIL import Image
import tensorflow as tf
import requests
import google.auth
from google.auth.transport.requests import Request

# Load environment variables
load_dotenv()

app = FastAPI()

# === CONFIG ===
USE_VERTEX = False  # <<< Change this to True to call Vertex instead of local!
IMG_SIZE = (224, 224)
LOCAL_MODEL_PATH = "models/vertex_ready_model"

# === Load Model (local) if needed ===
if not USE_VERTEX:
    print("🔵 Loading local TensorFlow model...")
    model = tf.saved_model.load(LOCAL_MODEL_PATH)
    predict_fn = model.signatures["serving_default"]
    print("✅ Local model loaded.")

# === Vertex Config ===
ENDPOINT_ID = os.getenv("ENDPOINT_ID")
PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")

CLASS_NAMES = ['Apple', 'Cherry', 'Corn', 'Cotton', 'Grape', 'Orange', 'Peach', 'Pepper,', 'Potato', 'Squash', 'Strawberry', 'Tomato', 'Wheat']


def predict_vertex(b64_instance):
    credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    credentials.refresh(Request())
    
    token = credentials.token

    endpoint_url = f"https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}:predict"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "instances": [{"b64": b64_instance}]
    }

    response = requests.post(endpoint_url, headers=headers, json=payload)
    if not response.ok:
        print("❌ Vertex AI responded with:", response.text)
        response.raise_for_status()

    return response.json()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image.")

    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents)).convert('RGB')
        img = img.resize(IMG_SIZE)

        resized_io = io.BytesIO()
        img.save(resized_io, format="JPEG", optimize=False, quality=85)

        resized_io.seek(0)

        resized_bytes = resized_io.getvalue()

        # # EXTRA: Try decoding the base64 string immediately
        # try:
        #     test_decoded_bytes = base64.b64decode(b64_encoded)
        #     print("🟢 Successfully base64-decoded image.")
        #     # Optional: Save to disk to double-check
        #     with open("test_decoded_image.jpg", "wb") as f:
        #         f.write(test_decoded_bytes)
        # except Exception as decode_error:
        #     print("❌ Base64 decoding error before model call:", decode_error)
        #     raise HTTPException(status_code=500, detail="Base64 encoding/decoding validation failed.")
        if USE_VERTEX:
            input_tensor = tf.constant([resized_bytes])
            b64_tensor = tf.io.encode_base64(input_tensor[0])
            b64_encoded = b64_tensor.numpy().decode('utf-8')
            result = predict_vertex(b64_encoded)
            predictions = result.get("predictions", [])
        else:

            b64_encoded = base64.b64encode(resized_bytes).decode('utf-8')
            b64_encoded = b64_encoded.replace('\n', '').replace('\r', '')

            input_tensor = tf.constant([resized_bytes])
            b64_tensor = tf.io.encode_base64(input_tensor[0])
            b64_encoded = b64_tensor.numpy().decode('utf-8')

            input_b64_tensor = tf.constant([b64_encoded])
            preds = predict_fn(b64=input_b64_tensor)
            predictions = preds["predictions"].numpy().tolist()


        

        # After getting 'predictions':


        top_class_idx = int(np.argmax(predictions[0]))
        top_class_label = CLASS_NAMES[top_class_idx]
        top_confidence = float(np.max(predictions[0])) * 100  # Scale to percentage

        return JSONResponse(content={
            "predicted_class": top_class_label,
            "confidence": f"{top_confidence:.2f}%",  # Format nicely
            "predictions": predictions
        })

    
            # input_tensor = tf.constant([b64_encoded])
            # preds = predict_fn(b64=input_tensor)
            # predictions = preds["predictions"].numpy().tolist()

        



    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
