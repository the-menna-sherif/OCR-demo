# OCR Comparison

## Comparison Scope

- Tesseract 5
- PaddleOCR
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
| PaddleOCR | Not tested | Not tested |
| CRAFT + TrOCR/PARSeq | Not tested | Not tested |
| Qwen2.5-VL + DeepSeek-OCR | Not tested | Not tested |

## Evaluation Criteria

- OCR accuracy
- Multilingual recognition
- Blur tolerance
- Invoice text extraction

## Conclusions

Tesseract 5 successfully extracted text from the clear invoice image but failed
completely on the multilingual blurry invoice image. The other OCR families have
not been implemented or tested yet.