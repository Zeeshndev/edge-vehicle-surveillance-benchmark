# Week 2 Log — FP32 Baseline Matrix Completion

**Project:** Edge Vehicle Surveillance Benchmark (YOLOv10 vs YOLOv11, UA-DETRAC)
**Phase:** Week 2 → Week 3 transition
**Status:** ✅ FP32 baseline matrix complete — proceeding to INT8 quantization & calibration

---

## 1. Summary

All four FP32 baseline models in our 2×2 experimental design (architecture × resolution) have finished training on dual T4 GPUs under identical hyperparameter controls (early stopping, `patience=15`). These four checkpoints now serve as the reference point against which every INT8 quantization result in Week 3–4 will be measured.

## 2. FP32 Baseline Results

| Model | Resolution | Epochs (stopped/max) | mAP50 | mAP50-95 | Car AP | Bus AP | Van AP | Others AP |
|---|---|---|---|---|---|---|---|---|
| YOLOv10n | 640×640 | 44/59 | 78.6% | 59.1% | 92.8 | 84.4 | 75.8 | 63.1 |
| YOLOv11n | 640×640 | 17/32 | 82.4% | 61.0% | 92.8 | 84.4 | 81.1 | 71.4 |
| YOLOv10n | 320×320 | 29/44 | 73.6% | 51.2% | 90.3 | 79.1 | 65.2 | 59.8 |
| YOLOv11n | 320×320 | 40/55 | 72.5% | 51.5% | 89.0 | 81.0 | 68.0 | 52.0 |

All four runs used the same UA-DETRAC train/val split, augmentation policy, optimizer, and learning-rate schedule, so differences below are attributable to architecture and input resolution rather than training-condition drift.

## 3. Generational Accuracy Gain (v10 → v11)

At the standard 640×640 resolution, YOLOv11n reached its early-stopping point in just **17 epochs** (vs. 44 for YOLOv10n) while still landing on a higher final score — 82.4% mAP50 / 61.0% mAP50-95 against YOLOv10n's 78.6% / 59.1%. The gain is concentrated in the harder minority classes: Van AP improves from 75.8 → 81.1 and Others AP from 63.1 → 71.4, while Car and Bus AP are identical across both architectures (92.8 and 84.4). This suggests v11's architectural changes are primarily helping it separate harder, less-represented vehicle classes rather than lifting the already-easy majority classes further — and it's doing so with meaningfully faster convergence.

## 4. Downscaling Sensitivity (640×640 → 320×320)

The two architectures respond very differently to the drop in input resolution:

- **YOLOv11n** loses **9.9 points of mAP50** (82.4% → 72.5%), essentially wiping out its generational advantage — at 320×320 it actually scores marginally *below* YOLOv10n.
- **YOLOv10n** loses only **5.0 points of mAP50** (78.6% → 73.6%), showing much better tolerance to reduced input resolution.

This crossover is the single most important finding of Week 2: **YOLOv11n's accuracy edge is resolution-dependent**. Its largest per-class drop is Others AP (71.4 → 52.0, a 19.4-point fall) and Van AP (81.1 → 68.0), suggesting its gains at 640×640 rely on spatial detail that a 320×320 input simply doesn't preserve for small/occluded vehicle classes. YOLOv10n's per-class degradation is comparatively gentle across the board.

**Implication for Week 3–4:** if the deployment target is a low-power edge device forced down to 320×320 for latency/thermal reasons, YOLOv10n may be the safer INT8 quantization candidate despite its lower ceiling at full resolution. Both architectures at both resolutions will still be carried forward through quantization so this can be confirmed empirically rather than assumed from FP32 numbers alone.

## 5. Pivot to Week 3: INT8 Post-Training Quantization

With the FP32 matrix locked, the immediate next step is constructing a **500-image calibration subset** drawn from the UA-DETRAC training split (not validation, to avoid calibration-on-test leakage). This subset will be used to calibrate activation ranges for both INT8 export paths:

- `INT8_TFLite`
- `INT8_ONNX`

for all four (architecture × resolution) combinations, keeping the calibration set fixed across both export paths so any accuracy delta between TFLite and ONNX INT8 is attributable to the quantization/runtime path and not to calibration-sample variance. The master experiment log has been extended with blank template rows for these eight upcoming runs, ready for Week 4 on-device Android telemetry (latency, p95 latency, battery drain, peak thermal state, memory).

---
*Log generated as part of the Edge Vehicle Surveillance Benchmark repository documentation.*
