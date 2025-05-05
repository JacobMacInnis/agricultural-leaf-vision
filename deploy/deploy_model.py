from google.cloud import aiplatform
import json
from pathlib import Path

PROJECT_ID = "agricultural-leaf-vision"
REGION = "us-central1"
MODEL_DISPLAY_NAME = "agricultural-leaf-vision-model"
MODEL_DIR = "models/vertex_ready_model"
ENDPOINT_INFO_PATH = Path("deploy/endpoint.json")

# Initialize Vertex AI client
aiplatform.init(project=PROJECT_ID, location=REGION)

# Upload model
model = aiplatform.Model.upload(
    display_name=MODEL_DISPLAY_NAME,
    artifact_uri=MODEL_DIR,
    serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-11:latest",
)

model = model.wait()  # Wait for upload to complete
print(f"✅ Model uploaded to Vertex AI: {model.resource_name}")

# Deploy model to an endpoint
endpoint = model.deploy(
    machine_type="n1-standard-2",
    min_replica_count=1,
    max_replica_count=1,
    traffic_split={"0": 100},
)

endpoint.wait()  # Wait for deployment to complete
print(f"✅ Model deployed to endpoint: {endpoint.resource_name}")

# Save endpoint ID for later use (e.g., backend server will load this)
ENDPOINT_INFO_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(ENDPOINT_INFO_PATH, "w") as f:
    json.dump({"endpoint": endpoint.resource_name}, f, indent=2)
