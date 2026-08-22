# OCR Monitoring

## Overview

The OCR demo measures the cost of each image-processing run in addition to
extracting text. `MetricsCollector` combines elapsed-time measurement with
periodic CPU and GPU utilization sampling, so the same monitoring workflow can
be used with all supported engines.

The collected metrics are:

- Elapsed processing time in seconds
- Average and maximum system CPU utilization
- Average and maximum utilization for every detected NVIDIA GPU
- Prompt, completion, and total token counts for Ollama-backed engines
- Device baseline information: logical CPU cores, RAM, GPU name, and VRAM

CPU monitoring remains available when no NVIDIA GPU or NVML driver is detected.

## Architecture

```mermaid
flowchart TD
	A[Select OCR engine] --> B[Create MetricsCollector]
	B --> C[Start OCR timer]
	B --> D[Start CPU/GPU sampler]
	C --> E[Extract text from invoice]
	D --> E
	E --> F[Stop timer and sampler]
	F --> G[Build OCRMetrics result]
	G --> H[Print timing and utilization report]
```

`ComputeMonitor` samples system usage every `0.2` seconds by default in a
background thread. `OCRTimer` measures the OCR operation with a monotonic
performance counter. The two summaries are combined into an `OCRMetrics`
instance when the context manager exits.

## Installation and Configuration

Install the project dependencies with:

```bash
uv sync
```

The monitoring stack uses `psutil` for CPU data and `pynvml` for NVIDIA GPU
data. PaddleOCR and PaddlePaddle are required when `paddleocr` is selected.
Ollama and the configured DeepSeek-OCR model are required when `vlms` is
selected.

In `main.py`, choose the engine and configure the input folder:

```python
engine_name = "paddleocr"  # or "tesseract", "transformers", or "vlms"
image_folder = Path(__file__).parent / "test-images"
process_image_folder(engine, image_folder, show_content=False)
```

Run the demo with:

```bash
uv run python main.py
```

## Recorded Device Baseline

| Resource | Recorded value |
|---|---|
| Logical CPU cores | 32 |
| System RAM | 63.7 GB |
| GPU | NVIDIA RTX 3500 Ada Generation Laptop GPU |
| GPU VRAM | 12.0 GB |

## Results

### Tesseract Folder Run

The following results were collected by iterating over all six images in the
project's `test-images` folder on the recorded device.

| Image | Time (s) | CPU average | CPU maximum | GPU average | GPU maximum |
|---|---:|---:|---:|---:|---:|
| `arabic-handwriting.jpg` | 1.450 | 18.3% | 36.8% | 15.5% | 26.0% |
| `invoice-phone-cam.jpg` | 0.520 | 6.0% | 9.2% | 4.3% | 11.0% |
| `invoice-phone-cam2.jpg` | 0.418 | 8.1% | 14.2% | 1.0% | 1.0% |
| `invoice-scan.jpg` | 0.515 | 40.3% | 100.0% | 1.0% | 1.0% |
| `skewed-arabic-form.jpg` | 0.773 | 6.3% | 9.2% | 3.2% | 4.0% |
| `spanish-computer-pic.jpg` | 0.845 | 7.3% | 11.6% | 4.4% | 11.0% |


### PaddleOCR Folder Run

The following results were collected by iterating over all six images in the
project's `test-images` folder on the recorded device.

| Image | Time (s) | CPU average | CPU maximum | GPU average | GPU maximum |
|---|---:|---:|---:|---:|---:|
| `arabic-handwriting.jpg` | 2.540 | 26.6% | 38.1% | 4.0% | 11.0% |
| `invoice-phone-cam.jpg` | 33.043 | 34.4% | 42.4% | 7.2% | 86.0% |
| `invoice-phone-cam2.jpg` | 29.661 | 36.9% | 50.7% | 15.8% | 52.0% |
| `invoice-scan.jpg` | 32.175 | 32.0% | 39.9% | 0.0% | 0.0% |
| `skewed-arabic-form.jpg` | 94.774 | 27.2% | 46.9% | 0.5% | 7.0% |
| `spanish-computer-pic.jpg` | 67.933 | 35.8% | 42.0% | 2.4% | 31.0% |

### DeepSeek-OCR Folder Run

The following results were collected by iterating over all six images in the
project's `test-images` folder. The device baseline was 32 logical CPU cores,
63.7 GB RAM, and an NVIDIA RTX 3500 Ada Generation Laptop GPU with 12.0 GB
VRAM.

| Image | Time (s) | CPU average | CPU maximum | GPU average | GPU maximum | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `arabic-handwriting.jpg` | 18.978 | 8.7% | 34.9% | 65.2% | 100.0% | 1190 | 2906 | 4096 |
| `invoice-phone-cam.jpg` | 2.329 | 8.5% | 12.0% | 80.1% | 100.0% | 910 | 296 | 1206 |
| `invoice-phone-cam2.jpg` | 2.481 | 8.2% | 17.5% | 70.7% | 92.0% | 1120 | 344 | 1464 |
| `invoice-scan.jpg` | 2.197 | 9.2% | 13.8% | 72.7% | 91.0% | 910 | 311 | 1221 |
| `skewed-arabic-form.jpg` | 15.955 | 12.3% | 28.0% | 82.2% | 93.0% | 910 | 3186 | 4096 |
| `spanish-computer-pic.jpg` | 5.113 | 8.9% | 15.4% | 81.0% | 100.0% | 910 | 1004 | 1914 |

## Engine Comparison

| Engine | Clear invoice (s) | Blurred invoice (s) | Average CPU | Peak CPU |
|---|---:|---:|---:|---:|
| Tesseract | 0.976 | 0.735 | 10.1% | 18.5% |
| PaddleOCR | 145.221 | 98.928 | 33.1% | 54.5% |
| DeepSeek-OCR | 4.808 | 3.157 | 16.5% | 32.0% |

These measurements show that Tesseract completed both runs substantially faster
and with lower CPU utilization in this environment. The results describe one
local run per image and should not be treated as a general benchmark.

