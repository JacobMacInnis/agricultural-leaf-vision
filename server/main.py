import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import io
import numpy as np
from PIL import Image
import tensorflow as tf

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

IMG_SIZE = (224, 224)
LOCAL_MODEL_PATH = "ml/models/best_model_saved.keras"

CLASS_NAMES = ['Apple', 'Cherry', 'Corn', 'Cotton', 'Grape', 'Orange', 'Peach', 'Pepper,', 'Potato', 'Squash', 'Strawberry', 'Tomato', 'Wheat']


print("🔵 Loading local TensorFlow model...")
model = tf.keras.models.load_model(LOCAL_MODEL_PATH)
# predict_fn = model.signatures["serving_default"]
print("✅ Local model loaded.")


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

        # Prepare the tensor properly (normalize pixels between 0-1)
        img_array = np.array(img) / 255.0  # Normalize to [0,1]
        input_tensor = tf.convert_to_tensor([img_array], dtype=tf.float32)  # batch dimension

        # Predict
        preds = model(input_tensor)
        preds = preds.numpy()
        print(preds)
        print(CLASS_NAMES)

        top_class_idx = int(np.argmax(preds[0]))
        top_class_label = CLASS_NAMES[top_class_idx]
        top_confidence = float(np.max(preds[0])) * 100
        # contents = await file.read()
        # img = Image.open(io.BytesIO(contents)).convert('RGB')
        # img = img.resize(IMG_SIZE)

        # img_bytes = io.BytesIO()
        # img.save(img_bytes, format="JPEG", optimize=False, quality=85)
        # img_bytes.seek(0)
        # image_data = img_bytes.getvalue()


        # # Prepare the image as base64 tensor for local model
        # input_tensor = tf.constant([tf.io.encode_base64(image_data).numpy().decode('utf-8')])
        # preds = model(b64=input_tensor)
        predictions = preds[0].tolist()


        # top_class_idx = int(np.argmax(predictions[0]))
        # top_class_label = CLASS_NAMES[top_class_idx]
        # top_confidence = float(np.max(predictions[0])) * 100


        return JSONResponse(content={
            "predicted_class": top_class_label,
            "confidence": f"{top_confidence:.2f}%",
            "predictions": predictions
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def start_server():
    uvicorn.run("backend.server:app", host="0.0.0.0", port=8080, reload=True)
