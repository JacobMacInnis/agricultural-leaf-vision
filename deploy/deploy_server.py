import subprocess

PROJECT_ID = "agricultural-leaf-vision"
REGION = "us-central1"
SERVICE_NAME = "agricultural-leaf-vision-backend"
ARTIFACT_REPO = "gcr.io"  # Using GCR (easy for now)

# Image name
IMAGE_NAME = f"{ARTIFACT_REPO}/{PROJECT_ID}/{SERVICE_NAME}"

def run_command(command):
    result = subprocess.run(command, shell=True, check=True, text=True)
    return result

# Build Docker image
print("🔨 Building Docker image...")
run_command(f"docker build -t {IMAGE_NAME} ./backend")

# Push Docker image
print("🚀 Pushing Docker image to GCR...")
run_command(f"docker push {IMAGE_NAME}")

# Deploy to Cloud Run
print("🌐 Deploying to Cloud Run...")
run_command(
    f"gcloud run deploy {SERVICE_NAME} "
    f"--image {IMAGE_NAME} "
    f"--region {REGION} "
    f"--platform managed "
    f"--allow-unauthenticated"
)

print("✅ Backend deployed successfully!")
