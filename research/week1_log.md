# Week 1 Log: Pipeline Foundations & Data Ingestion

## 1. Environment & Infrastructure
* **Compute Setup:** The training pipeline was established using dual NVIDIA T4 GPUs via the Kaggle platform.
* **Pathing Resolution:** A critical pathing conflict between Kaggle's dynamic session directories and the Ultralytics framework's expected absolute paths was identified. This was engineered around by implementing a symlink wrapper (`os.symlink`), projecting Kaggle's `/kaggle/working/` outputs into a stable `/content/` virtual directory. This ensures the codebase remains robust and seamlessly portable between Colab and Kaggle environments.

## 2. Dataset Ingestion & Processing
* **Dataset:** The UA-DETRAC dataset (10GB) was successfully ingested and parsed.
* **Annotation Conversion:** Custom Python parsing scripts were deployed to convert UA-DETRAC's native XML annotations into the normalized YOLO format (`class x_center y_center w h`).
* **Ignore-Regions:** As strictly required by the methodology, the UA-DETRAC ignore-region masks were explicitly handled to prevent the artificial inflation of false positives during evaluation.

## 3. Frame Subsampling Strategy
* **Implementation:** A `Stride=5` temporal subsampling algorithm was applied to the training sequence.
* **Rationale:** UA-DETRAC contains highly redundant, high-framerate sequences of stationary or slow-moving traffic. Extracting every 5th frame reduces severe class imbalance and overfitting on near-duplicate frames while preserving the full diversity of the vehicle classes, optimizing our GPU compute budget.

## 4. Current Status
* **FP32 Baselines:** YOLOv10n (640x640) training is complete and weights have been secured via GitHub Releases. YOLOv11n (640x640) is currently actively training.

## 5. Methodological & Evaluation Controls
* **Evaluation Ignore-Region Handling:** Predictions falling within annotated ignore regions are filtered during evaluation scoring to prevent artificial false-positive penalties.
* **Temporal Subsampling Boundary:** The `Stride=5` temporal subsampling algorithm is applied strictly to training sequences; validation and test evaluation sequences remain at full frame rate ($1\times$) to preserve real-world continuous traffic distribution.
* **Hyperparameter Parity:** Both YOLOv10n and YOLOv11n models are fine-tuned under an identical training recipe (SGD/AdamW auto-optimizer, cosine LR schedule, initial lr0=0.01, batch size 32, patience 15) to isolate architectural impact.
* **Catch-All Class Behavior:** Lower average precision on the `Others` category (e.g., tractors, heavy machinery) is attributable to extreme inter-class variance in the UA-DETRAC dataset rather than labeling artifacts.