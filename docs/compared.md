# OCR Comparison

## Comparison Scope

- Tesseract 5
- PaddleOCR 3
- CRAFT + TrOCR/PARSeq
- Qwen2.5-VL + DeepSeek-OCR

## Test Inputs

| Test input | Status |
|---|---|
| Clear invoice image | Tested |
| Multilingual blurry invoice image | Tested |

## Summary Comparison

| OCR family | Clear invoice | Multilingual blurry invoice |
|---|---|---|
| Tesseract 5 | Successful | Failed completely |
| PaddleOCR 3 | Successful | Successful |
| CRAFT + TrOCR/PARSeq | Not tested | Not tested |
| Qwen2.5-VL + DeepSeek-OCR | Not tested | Not tested |

## Evaluation Criteria

- OCR accuracy
- Multilingual recognition
- Blur tolerance
- Invoice text extraction
- Processing time
- CPU/GPU utilization

## Monitoring

Each OCR run is wrapped in `MetricsCollector`. The demo records elapsed
processing time, average and maximum system CPU utilization, and average and
maximum utilization for each detected NVIDIA GPU. If no NVIDIA GPU or NVML
driver is available, it falls back to CPU-only monitoring.

## Conclusions

Tesseract 5 successfully extracted text from the clear invoice image but failed
completely on the multilingual blurry invoice image. PaddleOCR has now been
added to the demo and can be selected through `engine_factory`, but its OCR
results have not yet been recorded in this comparison. Timing and CPU/GPU
utilization metrics are now collected for each configured invoice run.