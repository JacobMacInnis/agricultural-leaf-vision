# Agriculture Leaf Vision

**Agriculture Leaf Vision** is a lightweight computer vision API that identifies plant species (or diseases) based on uploaded leaf images. It's built using **transfer learning** with CNN EfficientNetB2. I trained it on a PlantVillage dataset, and deployed to a serverless cloud backend.

> The project was developed to deepen my understanding of image preprocessing, transfer learning, and end-to-end ML deployment with minimal cloud cost. Originally deployed to Vertex the costs we to great for a side project.

---

## Try the App

**Live Demo:**  
https://agricultural-leaf-vision-7fab2.web.app/

You can upload a leaf image and receive a class prediction from the live API.  
⚠️ **Note:** The model is **not trained to production quality** — it often predicts the same label ("Pepper") for all inputs. It is intentionally undertrained to demonstrate infrastructure, not accuracy.

---

## What It Does

- Takes an uploaded image (leaf)
- Preprocesses the image to the correct input size
- Applies data augmentation during training
- Uses a pretrained CNN backbone (MobileNetV2 or EfficientNet)
- Fine-tunes the model on a small labeled dataset (PlantVillage)
- Returns class prediction via a REST API

---

## Machine Learning Details

| Type              | Value                          |
| ----------------- | ------------------------------ |
| ML Category       | Supervised Learning            |
| Model Type        | Convolutional Neural Network   |
| Strategy          | Transfer Learning              |
| Backbone Models   | EfficientNetB0                 |
| Pretrained On     | ImageNet                       |
| Fine-Tuned On     | PlantVillage (plant disease)   |
| Data Augmentation | Rotation, flip, zoom, contrast |
| Loss Function     | Categorical crossentropy       |

---

## Model Evaluation

While the training curves suggest promising performance, the confusion matrix reveals signs of overfitting — the model learned the training data well but fails to generalize to unseen examples.

### Accuracy Curve

<p align="center">
  <img src="/client/public/plots/accuracy_curve.png" alt="accuracy curve graph" width="600"/>
</p>

### Loss Curve

<p align="center">
  <img src="/client/public/plots/loss_curve.png" alt="loss curve graph" width="600"/>
</p>

### Confusion Matrix

<p align="center">
  <img src="/client/public/plots/confusion_matrix.png" alt="confusion matrix diagram" width="600"/>
</p>

🧠 Note: The model shows high training accuracy and low loss, but the confusion matrix highlights that the classifier consistently mispredicts most classes — suggesting the model is overfitting to a narrow subset of the training distribution.

---

## 🧪 Preprocessing & Training Pipeline

To adapt a generic vision model to agricultural data I applied these techniques:

- **Image resizing and normalization** to match backbone input specs
- **Augmentation**: horizontal/vertical flips, zoom, rotation, contrast variation
- **Batching** with stratified shuffling
- Used **early stopping** and **learning rate scheduling**

> Full training from scratch was avoided. Transfer learning was sufficient given dataset size.

---

## Tech Stack

- **Python 3.10**
- **TensorFlow / Keras**
- `tf.keras.applications` (MobileNetV2, EfficientNetB0)
- **Docker** (containerizing the API)
- **FastAPI** (optional REST layer)
- **Google Cloud Run** (serverless model hosting)
- **Artifact Registry** (image storage)
- **Firebase** (optional demo frontend)
- **Vite** (for future frontend deployment)

---

## Lessons Learned

- Observed how dataset quality directly impacts model output
- Evaluated tradeoffs between **model size** and **accuracy**
- **transfer learning** in a resource-constrained setting
- Built a **Dockerized ML inference API**
- Deployed with **Cloud Run** using minimal budget
- Fine-tuned image classification with **augmented data**
- Explored tradeoffs between **accuracy vs model size**
- Realized importance of **input resolution and normalization** for pre-trained CNNs

---

## Known Limitations

- The model is **not accurate** — due to minimal training and limited dataset coverage
- It frequently predicts the same class ("Pepper") regardless of input
- Dataset coverage is limited to a few categories and model
- This project is **for educational/demo purposes only** and not suitable for real agricultural use
- Best results come from clear, close-up leaf images

---

## 📚 Dataset

- **PlantVillage Dataset**  
  [Kaggle Link](https://www.kaggle.com/datasets/emmarex/plantdisease)

---
