import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# === CONFIG ===
OUTPUT_DIR = "frontend/public/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === FAKE SAMPLE DATA (REPLACE THIS WITH YOUR REAL DATA) ===
# Simulated training logs (you'll replace this with actual training history)
epochs = np.arange(1, 21)
train_accuracy = np.linspace(0.5, 0.95, 20) + np.random.normal(0, 0.02, 20)
val_accuracy = np.linspace(0.45, 0.92, 20) + np.random.normal(0, 0.03, 20)

train_loss = np.linspace(1.0, 0.2, 20) + np.random.normal(0, 0.02, 20)
val_loss = np.linspace(1.2, 0.3, 20) + np.random.normal(0, 0.03, 20)

# Simulated confusion matrix (you'll replace with real model results)
y_true = np.random.choice(5, 100)
y_pred = y_true.copy()
noise = np.random.choice(5, 20)
indices = np.random.choice(len(y_true), 20)
y_pred[indices] = noise

class_names = ['Apple', 'Cherry', 'Corn', 'Cotton', 'Wheat']


# === 1. Accuracy Curve ===
plt.figure(figsize=(8,6))
plt.plot(epochs, train_accuracy, label='Training Accuracy')
plt.plot(epochs, val_accuracy, label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Training and Validation Accuracy')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(OUTPUT_DIR, 'accuracy_curve.png'))
plt.close()

# === 2. Loss Curve ===
plt.figure(figsize=(8,6))
plt.plot(epochs, train_loss, label='Training Loss')
plt.plot(epochs, val_loss, label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training and Validation Loss')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(OUTPUT_DIR, 'loss_curve.png'))
plt.close()

# === 3. Confusion Matrix ===
cm = confusion_matrix(y_true, y_pred, labels=list(range(len(class_names))))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)

fig, ax = plt.subplots(figsize=(8,6))
disp.plot(ax=ax, cmap='Blues', colorbar=False)
plt.title('Confusion Matrix')
plt.savefig(os.path.join(OUTPUT_DIR, 'confusion_matrix.png'))
plt.close()

print("✅ All plots saved to", OUTPUT_DIR)
