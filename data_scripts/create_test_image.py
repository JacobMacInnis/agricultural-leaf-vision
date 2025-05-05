from PIL import Image
import numpy as np
import json

# Load and preprocess
img = Image.open('data/processed/test/Cherry/11075_5.jpg').convert('RGB')
img = img.resize((224, 224))
arr = np.array(img) / 255.0  # Normalize [0-1]

# Create JSON payload
payload = {
    "instances": [arr.tolist()]
}

# Save to file
with open('test_payload.json', 'w') as f:
    json.dump(payload, f)

print("✅ Payload saved to test_payload.json")
