## Project Structure & Implementation Status

| Path | Status | Description |
| :--- | :--- | :--- |
| `/data` | ✅ Implemented | UA-DETRAC parser, ignore-region masking, sequence-level splits (`split_manifest.json`) |
| `/model` | ✅ Implemented | YOLOv10n/YOLOv11n FP32 training pipelines ($640 \times 640$, $320 \times 320$) |
| `/research` | 🔄 Active | Literature review, methodology logs, experiment tracking schema |
| `/tests` | 🔄 Active | Unit tests for split validation, subsampling, and annotation integrity |
| `/android` | 📋 Planned (Week 4) | Telemetry-instrumented benchmarking harness (latency, thermal, battery) |
| `/paper` | 📋 Planned (Week 9) | TMLR LaTeX manuscript source and artifact citations |
