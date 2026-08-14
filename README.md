# Beyond Simulated Latency: Edge-Device Vehicle Surveillance Benchmark

This repository contains the dataset ingestion scripts, quantization pipelines, and Android telemetry harness for benchmarking INT8-quantized lightweight object detection models natively on consumer hardware.

## Project Structure
* `/research` - Literature reviews, experimental logs, and anomaly tracking.
* `/data` - Parsing and ingestion scripts for the UA-DETRAC dataset. *(Note: Raw dataset files are not hosted here due to size limitations).*
* `/model` - FP32 training pipelines and INT8 TFLite/ONNX quantization scripts for YOLOv10 and YOLOv11.
* `/android` - A generalized, telemetry-instrumented Android benchmarking harness for capturing real-time device battery, thermal, and memory strains.
* `/paper` - LaTeX source files for the resulting academic manuscript.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.