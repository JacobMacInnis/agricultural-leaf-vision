interface PredictionResultProps {
  predictedClass: string;
  confidence: string;
}

export default function PredictionResult({
  predictedClass,
  confidence,
}: PredictionResultProps) {
  if (!predictedClass) {
    return <div className="prediction-result"></div>;
  }

  return (
    <div className="prediction-result">
      Prediction: {predictedClass} ({confidence} confidence)
    </div>
  );
}
