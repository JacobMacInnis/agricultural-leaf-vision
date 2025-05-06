export default function ModelPerformance() {
  return (
    <div className="model-performance">
      <h2>Model Performance 📈</h2>
      <div className="plots-grid">
        <img src="/plots/accuracy_curve.png" alt="Accuracy Curve" />
        <img src="/plots/loss_curve.png" alt="Loss Curve" />
        <img src="/plots/confusion_matrix.png" alt="Confusion Matrix" />
      </div>
    </div>
  );
}
