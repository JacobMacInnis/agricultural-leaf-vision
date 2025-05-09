import { useState, useRef } from "react";
import { predictImage } from "../apis/predictImage";
import PredictionResult from "./PredictionResult";

const exampleImages = [
  { filename: "apple.jpg", label: "Apple" },
  { filename: "cherry.jpg", label: "Cherry" },
  { filename: "corn.jpg", label: "Corn" },
  { filename: "cotton.jpg", label: "Cotton" },
  { filename: "grape.jpg", label: "Grape" },
  { filename: "orange.jpg", label: "Orange" },
  { filename: "peach.jpg", label: "Peach" },
  { filename: "pepper.jpg", label: "Pepper" },
  { filename: "potato.jpg", label: "Potato" },
  { filename: "squash.jpg", label: "Squash" },
  { filename: "strawberry.jpg", label: "Strawberry" },
  { filename: "tomato.jpg", label: "Tomato" },
  { filename: "wheat.jpg", label: "Wheat" },
];

export default function UploadArea() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [predictedClass, setPredictedClass] = useState("");
  const [confidence, setConfidence] = useState("");

  const handlePrediction = (predicted: string, confidence: string) => {
    setPredictedClass(predicted);
    setConfidence(confidence);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreviewUrl(URL.createObjectURL(selectedFile));
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handlePredict = async () => {
    if (!file) return;
    setLoading(true);
    setPredictedClass("");
    setConfidence("");
    try {
      const result = await predictImage(file);
      handlePrediction(result.predicted_class, result.confidence);
    } catch (error) {
      console.error("Prediction failed:", error);
      alert("Prediction failed. Try again.");
    }
    setLoading(false);
  };

  const handleExampleClick = async (exampleName: string) => {
    const imageUrl = `/examples/${exampleName}`;
    setPreviewUrl(imageUrl);

    // Fetch the image and turn it into a File object
    const response = await fetch(imageUrl);
    const blob = await response.blob();
    const exampleFile = new File([blob], exampleName, { type: blob.type });

    setFile(exampleFile);
  };

  return (
    <div className="card upload-area">
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        ref={fileInputRef}
        style={{ display: "none" }}
      />
      <button className="button" onClick={handleUploadClick}>
        Upload Image
      </button>
      <PredictionResult
        predictedClass={predictedClass}
        confidence={confidence}
        loading={loading}
      />
      <div className="preview-box">
        {previewUrl ? (
          <img src={previewUrl} alt="Preview" className="preview-image" />
        ) : (
          <span>No image selected</span>
        )}
      </div>
      <button
        className="button"
        onClick={handlePredict}
        disabled={!file || loading}
      >
        {loading ? "Predicting..." : "Predict"}
      </button>

      {loading && (
        <div className="loading-message">
          🛠️ Starting the server... (cold start may take 30–45 seconds)
        </div>
      )}

      <div className="example-images">
        <h3>Or Try an Example Image:</h3>
        <div className="example-grid">
          {exampleImages.map(({ filename, label }) => (
            <div key={filename} className="example-thumbnail-container">
              <img
                key={filename}
                src={`/examples/${filename}`}
                alt={label}
                className="example-thumbnail"
                onClick={() => handleExampleClick(filename)}
              />
              <div className="example-label">{label}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
