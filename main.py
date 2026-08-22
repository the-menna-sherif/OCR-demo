import warnings
from pathlib import Path

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


def process_image_folder(engine, image_folder, show_content=False):
    image_folder = Path(image_folder)
    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
    image_paths = sorted(
        path for path in image_folder.iterdir()
        if path.is_file() and path.suffix.lower() in image_extensions
    )

    if not image_paths:
        raise FileNotFoundError(f"No supported images found in {image_folder}")

    for image_path in image_paths:
        print(f"\n===== {image_path.name} =====")
        with MetricsCollector(engine, image_path) as metrics:
            text = engine.extract_text(image_path)

        if show_content:
            print("Image content:")
            print(text.strip() or "[No text detected]")
        print("Metrics:")
        print(metrics.result.report())


def main():
    engine_name = "tesseract"  # options: paddleocr, tesseract, transformers, vlms
    engine = engine_factory(engine_name)
    print(f"Using OCR engine: {engine_name}")

    print("*************** device specs *******************")
    print(get_device_specs().report())
    image_folder = Path(__file__).parent / "test-images"
    process_image_folder(engine, image_folder, show_content=False)



if __name__ == "__main__":
    main()
