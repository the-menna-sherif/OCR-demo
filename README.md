# OCR-demo

A small Python demo for comparing optical character recognition (OCR) engines
with timing and hardware-utilization metrics.

## What Is This?

The demo currently supports Tesseract and PaddleOCR. It extracts text from
clear and blurred invoice images and reports the runtime and compute usage for
each OCR run.

## Tech Stack

- Python 3.12+
- [pytesseract](https://pypi.org/project/pytesseract/)
- [PaddleOCR](https://pypi.org/project/paddleocr/)
- [Pillow](https://pypi.org/project/Pillow/)
- `psutil` and `pynvml` for monitoring
- Tesseract OCR

## Project Structure

```text
ocr-demo/
├── main.py
├── engines/          # Tesseract and PaddleOCR adapters
├── monitoring/       # Timing, CPU/GPU, and device metrics
├── docs/              # OCR comparison notes
├── pyproject.toml
└── README.md
```

## Setup

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Python 3.12 or newer
- Tesseract OCR installed and available on `PATH`
- Invoice images at the paths configured in `main.py`

### Installation

```bash
uv sync
```

### Running

```bash
uv run python main.py
```

`main.py` currently uses PaddleOCR. Change `engine_name` to `"tesseract"` to
run the Tesseract adapter instead. The command processes both configured
invoice images, prints the extracted text for the blurred image, and reports
device specifications followed by per-image metrics.

### Metrics

Each OCR run is wrapped in `MetricsCollector`, which reports:

- Elapsed processing time
- Average and maximum system CPU utilization
- Average and maximum utilization for each detected NVIDIA GPU

When no NVIDIA GPU or NVML driver is available, monitoring continues with CPU
metrics only.

## Limitations

This is a local comparison demo. Image paths are currently configured directly
in the engine and entry-point modules, and the comparison dataset is limited
to the invoice images described in [docs/compared.md](docs/compared.md).