import pytesseract
from PIL import Image

scanned_invoice_clear = r"C:\Users\MennaSherif\Downloads\invoice-phone-cam.jpg"
scanned_invoice_blurred = r"C:\Users\MennaSherif\Downloads\invoice-phone-cam2.jpg"


class TesseractEngine:
    def __init__(self):
        self.tesseract_cmd = r"C:\Users\MennaSherif\AppData\Local\Tesseract-OCR\tesseract.exe"
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd

    def check_version(self):
        # Check if Tesseract is installed and reachable
        try:
            version = pytesseract.get_tesseract_version()
            return f"Tesseract version: {version}"
        except Exception as e:
            return f"Error: {e}"

    def extract_text(self, image_path):
        # Load an image and perform OCR
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text


def main():
    engine = TesseractEngine()

    # # Check Tesseract version
    # version_info = engine.check_version()
    # print(version_info)

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