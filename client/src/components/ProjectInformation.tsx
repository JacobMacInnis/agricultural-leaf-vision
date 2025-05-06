export default function ProjectInformation() {
  return (
    <div className="model-info-card">
      <h2>About the Project 🧠</h2>
      <ul>
        <li>
          <strong>Task:</strong> Image Classification of Plant Leaves
        </li>
        <li>
          <strong>Architecture:</strong> Transfer Learning with EfficientNetB0
          (Convolutional Neural Network)
        </li>
        <li>
          <strong>Technique:</strong> Fine-tuning pre-trained model on
          PlantVillage dataset (Resized and augmented)
        </li>
        <li>
          <strong>Dataset:</strong> Customized subset of PlantVillage Plant
          Disease Dataset
        </li>
        <li>
          <strong>Preprocessing:</strong> Image resizing to 224x224, JPEG
          compression optimization
        </li>
        <li>
          <strong>Frameworks:</strong> TensorFlow / Keras, FastAPI, Vite React
          Frontend
        </li>
        <li>
          <strong>Backend Hosting:</strong> Google Cloud Run, Google Artifact
          Registry,
        </li>
        <li>
          <strong>Frontend Hosting:</strong> Google Firebase
        </li>
        <li>
          <strong>Experience Gained:</strong> CNN Image classification,
          parameter tuning, Cloud deployment/hosting, Model serving
        </li>
      </ul>
    </div>
  );
}
