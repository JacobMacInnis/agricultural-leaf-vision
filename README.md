# 🌾 Agricultural Leaf Vision

Agricultural Leaf Vision is an AI-powered application that classifies plant species and detects leaf health from images.  
Built with TensorFlow, Docker, and GCP Cloud Run, it helps farmers, researchers, and agricultural technologists monitor crop conditions quickly and easily.

Supported species include Apple, Orange, Peach, Corn, Potato, Grape, Strawberry, Tomato, Cherry, Wheat, Squash, Cotton, and Pepper.

<!-- local server -->

PYTHONPATH=. poetry run uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload
