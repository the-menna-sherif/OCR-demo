import warnings

# Filter out warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from engines.tesseract import TesseractEngine
from engines.paddleOCR import PaddleOCREngine
from engines.trnsfrmrs import TransformersEngine
from engines.vlms import DeepSeekOCREngine
from monitoring.metrics import MetricsCollector
from monitoring.whoami import get_device_specs

def engine_factory(engine_name):
    if engine_name == "tesseract":
        return TesseractEngine()
    if engine_name == "paddleocr":
        return PaddleOCREngine()
    if engine_name == "transformers":
        return TransformersEngine()
    if engine_name == "vlms":
        return DeepSeekOCREngine()
    else:
        raise ValueError(f"Unsupported engine: {engine_name}")

def main():
    # engine selection
    engine_name = "vlms"  # options: paddleocr, tesseract, transformers, vlms
    engine = engine_factory(engine_name)
    print(f"Using OCR engine: {engine_name}")


    # clear scanned invoice
    clear_path = r"C:\Users\MennaSherif\Downloads\invoice-phone-cam.jpg"
    with MetricsCollector(engine, clear_path) as clear_metrics:
        clear_text = engine.extract_text(clear_path)
    # print("Extracted text from clear invoice:")
    # print(clear_text)

    # blurred scanned invoice
    blurred_path = r"C:\Users\MennaSherif\Downloads\invoice-phone-cam2.jpg"
    with MetricsCollector(engine, blurred_path) as blurred_metrics:
        blurred_text = engine.extract_text(blurred_path)
    print("Extracted text from blurred invoice:")
    print(blurred_text)

    # device baseline specs, printed first as a frame of reference for the metrics below
    print("*************** device specs *******************")
    print(get_device_specs().report())

    # metric prints
    print("*************** metrics *******************")

    print(clear_metrics.result.report())
    print(blurred_metrics.result.report())



if __name__ == "__main__":
    main()
