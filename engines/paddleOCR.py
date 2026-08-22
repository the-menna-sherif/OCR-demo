from paddleocr import PaddleOCR
import paddleocr


scanned_invoice_clear = r"C:\Users\MennaSherif\Downloads\invoice-phone-cam.jpg"
scanned_invoice_blurred = r"C:\Users\MennaSherif\Downloads\invoice-phone-cam2.jpg"


class PaddleOCREngine:
    _ocr_cache = {}

    def __init__(self, lang="en"):
        if lang not in PaddleOCREngine._ocr_cache:
            PaddleOCREngine._ocr_cache[lang] = PaddleOCR(
                use_textline_orientation=True,
                lang=lang,
                # oneDNN's new-IR executor can't convert some array<double>
                # attributes yet (NotImplementedError in onednn_instruction.cc),
                # so keep CPU inference on the plain Paddle backend.
                engine_config={"paddle_static": {"run_mode": "paddle"}},
            )
        self.ocr = PaddleOCREngine._ocr_cache[lang]

    def check_version(self):
        # Check if PaddleOCR is installed and reachable
        try:
            return f"PaddleOCR version: {paddleocr.__version__}"
        except Exception as e:
            return f"Error: {e}"

    def extract_text(self, image_path):
        # Load an image and perform OCR
        results = self.ocr.predict(image_path)
        lines = []
        for page in results:
            lines.extend(page["rec_texts"])
        return "\n".join(lines)


def main():
    engine = PaddleOCREngine()

    # # Check PaddleOCR version
    # version_info = engine.check_version()
    # print(version_info) # PaddleOCR version: 3.7.0

    # Extract text from the clear scanned invoice
    clear_text = engine.extract_text(scanned_invoice_clear)
    print("Extracted text from clear invoice:")
    print(clear_text)

    # Extract text from the blurred scanned invoice
    blurred_text = engine.extract_text(scanned_invoice_blurred)
    print("Extracted text from blurred invoice:")
    print(blurred_text)

if __name__ == "__main__":
    main()
