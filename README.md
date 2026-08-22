# OCR-demo

A small Python demo for comparing optical character recognition (OCR) engines
with timing and hardware-utilization metrics.

## What Is This?

The demo supports Tesseract, PaddleOCR, Transformers, and DeepSeek-OCR through
Ollama. It passes image paths from disk to the selected engine, extracts text
from clear and blurred invoice images, and reports runtime and compute usage
for each OCR run.

## Tech Stack

- Python 3.12+
- [pytesseract](https://pypi.org/project/pytesseract/)
- [PaddleOCR](https://pypi.org/project/paddleocr/)
- [Transformers](https://pypi.org/project/transformers/)
- [Ollama Python library](https://pypi.org/project/ollama/) and a local Ollama server
- [Pillow](https://pypi.org/project/Pillow/)
- `psutil` and `pynvml` for CPU/GPU monitoring
- Tesseract OCR

## Project Structure

```text
ocr-demo/
├── main.py
├── engines/          # OCR engine adapters
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
- Ollama installed and running when using DeepSeek-OCR
- The configured DeepSeek-OCR model available in Ollama when using `vlms`
- Invoice images at the paths configured in `main.py`

### Installation

```bash
uv sync
```

### Running

```bash
uv run python main.py
```

`main.py` currently uses DeepSeek-OCR through Ollama. Change `engine_name` to
`"tesseract"`, `"paddleocr"`, or `"transformers"` to run another adapter. The
supported values are:

```python
"tesseract"
"paddleocr"
"transformers"
"vlms"
```

The image paths are passed directly from disk in `main.py` through
`engine.extract_text(path)`. The command processes both configured invoice
images, prints the extracted text for the blurred image, and reports device
specifications followed by per-image timing and CPU/GPU metrics.

For DeepSeek-OCR, configure the optional environment variables before running:

```powershell
$env:OLLAMA_HOST = "http://localhost:11434"
$env:DEEPSEEK_OCR_MODEL = "deepseek-ocr"
```

The VLM adapter also supports free OCR, Markdown conversion, figure parsing,
multilingual OCR, image captioning, object detection, grounding, and custom
prompts when called directly.

### Metrics

Each OCR run is wrapped in `MetricsCollector`, which reports:

- Elapsed processing time
- Average and maximum system CPU utilization
- Average and maximum utilization for each detected NVIDIA GPU

When no NVIDIA GPU or NVML driver is available, monitoring continues with CPU
metrics only.

See [docs/monitored.md](docs/monitored.md) for the recorded device baseline
and per-engine measurements. See [docs/compared.md](docs/compared.md) for OCR
results and recommendations by use case.

## Limitations

This is a local comparison demo. Image paths are currently configured directly
in `main.py`, and the comparison dataset is limited to the invoice images
described in [docs/compared.md](docs/compared.md). The recorded results are
single local runs and are not a general benchmark.