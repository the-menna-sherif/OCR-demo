# OCR-demo

A small Python demo for exploring optical character recognition (OCR) with
[Tesseract](https://github.com/tesseract-ocr/tesseract), `pytesseract`, and Pillow.

## What Is This?

This project is a starting point for extracting text from images. The current
entry point is a minimal scaffold; image processing and OCR flow will be added
as the demo develops.

## Tech Stack

- Python 3.12+
- [pytesseract](https://pypi.org/project/pytesseract/)
- [Pillow](https://pypi.org/project/Pillow/)
- Tesseract OCR

## Project Structure

```text
ocr-demo/
├── main.py           # Demo entry point
├── pyproject.toml    # Project metadata and dependencies
└── README.md         # Project documentation
```

## Setup

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Python 3.12 or newer
- Tesseract OCR installed and available on `PATH`

### Installation

```bash
uv sync
```

### Running

```bash
uv run python main.py
```

The current command runs the project scaffold. The intended next step is to
pass an image to Tesseract and display the extracted text.

## Limitations

This is an early local demo. It does not yet accept image input or return OCR
results.