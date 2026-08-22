# OCR Comparison

## Comparison Scope

- Tesseract 5
- PaddleOCR 3
- CRAFT + TrOCR/PARSeq
- DeepSeek-OCR through Ollama

## Test Inputs

All six images in the project's `test-images` folder were processed by the
Tesseract, PaddleOCR, and DeepSeek-OCR engines.

| Test input | Tesseract | PaddleOCR | DeepSeek-OCR |
|---|---|---|---|
| `arabic-handwriting.jpg` | Tested | Tested | Tested |
| `invoice-phone-cam.jpg` | Tested | Tested | Tested |
| `invoice-phone-cam2.jpg` | Tested | Tested | Tested |
| `invoice-scan.jpg` | Tested | Tested | Tested |
| `skewed-arabic-form.jpg` | Tested | Tested | Tested |
| `spanish-computer-pic.jpg` | Tested | Tested | Tested |

## Summary Comparison

| OCR family | Images tested | Total time (s) | Average time (s) | Average CPU | Average GPU |
|---|---:|---:|---:|---:|---:|
| Tesseract 5 | 6 | 4.521 | 0.754 | 14.4% | 4.9% |
| PaddleOCR 3 | 6 | 260.126 | 43.354 | 32.2% | 5.0% |
| DeepSeek-OCR through Ollama | 6 | 47.053 | 7.842 | 9.3% | 75.3% |
| CRAFT + TrOCR/PARSeq | 0 | Not tested | Not tested | Not tested | Not tested |

### Recommendations by Use Case

| Use case | Recommended engine | Reason |
|---|---|---|
| Lowest processing time | Tesseract 5 | Lowest measured average and total processing time across all six images. |
| GPU-accelerated processing | DeepSeek-OCR through Ollama | Highest measured average GPU utilization in this environment. |
| CPU-focused processing | Tesseract 5 | Lowest measured average CPU utilization among the three tested engines. |
| Structured or multilingual OCR | DeepSeek-OCR through Ollama | Use when its OCR output quality and layout handling justify the additional processing time. |

## Evaluation Criteria

- OCR accuracy
- Multilingual recognition
- Blur tolerance
- Invoice text extraction
- Processing time and resource utilization

## Conclusions

Across the six-image folder run, Tesseract 5 was fastest and had the lowest
average CPU utilization. DeepSeek-OCR through Ollama took longer but used the
GPU substantially more than the other engines. PaddleOCR had the highest
average processing time and CPU utilization in this run. These measurements
describe one local run per image; OCR quality and layout preservation require
separate inspection of the extracted text.