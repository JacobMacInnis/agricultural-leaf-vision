import { useState } from "react";
import UploadArea from "./components/UploadArea";
import PredictionResult from "./components/PredictionResult";
import ModelPerformance from "./components/ModelPerformance";
import "./index.css";
import ProjectInformation from "./components/ProjectInformation";

function App() {
  const [predictedClass, setPredictedClass] = useState("");
  const [confidence, setConfidence] = useState("");

  const handlePrediction = (predicted: string, confidence: string) => {
    setPredictedClass(predicted);
    setConfidence(confidence);
  };

  return (
    <div className="container">
      <header className="intro-header">
        <h1 className="main-title">Agricultural Leaf Vision 🌿</h1>

        <p className="subtitle">
          Classify agricultural crop leaves into 13 specific categories
        </p>

        <p className="poc-notice">
          ⚡ This is a Proof of Concept (POC) demonstrating AI-based leaf
          classification.
        </p>

        <p className="trained-on">
          🥬 Trained to recognize: Apple, Cherry, Corn, Cotton, Grape, Orange,
          Peach, Pepper, Potato, Squash, Strawberry, Tomato, Wheat.
        </p>

        <p className="warning">
          ❌ Other plants or general leaves are not supported in this demo.
        </p>
      </header>

      <UploadArea onPrediction={handlePrediction} />

      <PredictionResult
        predictedClass={predictedClass}
        confidence={confidence}
      />

      <hr className="divider" />

      <ProjectInformation />
      <ModelPerformance />

      <footer className="footer">© 2025 Agricultural Leaf Vision</footer>
    </div>
  );
}

export default App;
