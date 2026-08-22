import numpy as np
import torch
from PIL import Image

from craft_text_detector import Craft, read_image
from craft_text_detector.file_utils import rectify_poly

try:
    from strhub.data.module import SceneTextDataModule
except ImportError:
    SceneTextDataModule = None

scanned_invoice_clear = r"C:\Users\MennaSherif\Downloads\invoice-phone-cam.jpg"
scanned_invoice_blurred = r"C:\Users\MennaSherif\Downloads\invoice-phone-cam2.jpg"


class TransformersEngine:
    """CRAFT for text detection + PARSeq for recognition, both run on GPU when available."""

    _model_cache = {}

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        if self.device not in TransformersEngine._model_cache:
            craft = Craft(cuda=self.device.type == "cuda", refiner=True, crop_type="poly")

            parseq = torch.hub.load("baudm/parseq", "parseq", pretrained=True, trust_repo=True)
            parseq = parseq.eval().to(self.device)

            # only importable after torch.hub.load has cached/pathed the parseq repo
            

            transform = SceneTextDataModule.get_transform(parseq.hparams.img_size)

            TransformersEngine._model_cache[self.device] = (craft, parseq, transform)

        self.craft, self.parseq, self.transform = TransformersEngine._model_cache[self.device]

    def check_version(self):
        # Check if PyTorch can see a GPU and report the device PARSeq will run on
        try:
            return f"PyTorch version: {torch.__version__} | Device: {self.device}"
        except Exception as e:
            return f"Error: {e}"

    def extract_text(self, image_path):
        # Detect text regions with CRAFT, then recognize each region with PARSeq
        image = read_image(image_path)
        detection = self.craft.detect_text(image)

        # order regions top-to-bottom, left-to-right for readable output
        regions = sorted(
            detection["polys"],
            key=lambda poly: (np.array(poly)[:, 1].min(), np.array(poly)[:, 0].min()),
        )

        lines = []
        for poly in regions:
            poly = np.array(poly, dtype=np.float32)
            if len(poly) < 4:
                continue

            crop = rectify_poly(image, poly)
            if crop.size == 0:
                continue

            tensor = self.transform(Image.fromarray(crop)).unsqueeze(0).to(self.device)
            with torch.no_grad():
                logits = self.parseq(tensor)
            label, _ = self.parseq.tokenizer.decode(logits.softmax(-1))
            if label and label[0]:
                lines.append(label[0])

        return "\n".join(lines)


def main():
    engine = TransformersEngine()

    # # Check PyTorch version and device
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
