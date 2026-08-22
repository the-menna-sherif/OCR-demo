# OCR Comparison

## Comparison Scope

- Tesseract 5
- PaddleOCR 3
- CRAFT + TrOCR/PARSeq
- DeepSeek-OCR through Ollama

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
| DeepSeek-OCR through Ollama | Successful | Successful (includes table boundaries) |

### Recommendations by Use Case

| Use case | Recommended engine | Reason |
|---|---|---|
| Clear invoice with plain text | Tesseract 5 | Successfully extracted the text and is the simplest OCR option for clear images. |
| Multilingual or blurry invoice | DeepSeek-OCR through Ollama | Successfully processed the blurry invoice, while Tesseract failed completely. |
| Invoice with tables or structured layout | DeepSeek-OCR through Ollama | Successfully processed both invoices and preserved the table boundaries. |
| General-purpose invoice OCR | PaddleOCR 3 or DeepSeek-OCR through Ollama | Both successfully processed the clear and blurry invoices; choose based on deployment needs. |

## Evaluation Criteria

- OCR accuracy
- Multilingual recognition
- Blur tolerance
- Invoice text extraction

## Conclusions

Tesseract 5 successfully extracted text from the clear invoice image but failed
completely on the multilingual blurry invoice image. PaddleOCR successfully
processed both images, and DeepSeek-OCR successfully processed both images
while preserving table boundaries.