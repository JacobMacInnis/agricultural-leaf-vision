import subprocess

PROJECT_ID = "agricultural-leaf-vision"
REGION = "us-east1"
SERVICE_NAME = "agricultural-leaf-vision-backend"
REPO_NAME = "agricultural-leaf-vision-repo"
# ARTIFACT_REPO = "gcr.io"

# Image name
IMAGE_NAME = f"{REGION}-docker.pkg.dev/{PROJECT_ID}/{REPO_NAME}/{SERVICE_NAME}"

def run_command(command):
    result = subprocess.run(command, shell=True, check=True, text=True)
    return result

# Build Docker image
print("🔨 Building Docker image...")
run_command(f"docker build --platform=linux/amd64 -t {IMAGE_NAME} .")

# Push Docker image
print("🚀 Pushing Docker image to GCR...")
run_command(f"docker push {IMAGE_NAME}")

# Deploy to Cloud Run
print("🌐 Deploying to Cloud Run...")
run_command(
    f"gcloud run deploy {SERVICE_NAME} "
    f"--image {IMAGE_NAME} "
    f"--region {REGION} "
    f"--memory 1Gi "
    f"--platform managed "
    f"--allow-unauthenticated"
)

print("✅ Backend deployed successfully!")
