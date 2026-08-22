import io
import os
import sys
from pathlib import Path

from ollama import Client
from PIL import Image, UnidentifiedImageError


OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.environ.get("DEEPSEEK_OCR_MODEL", "deepseek-ocr")
IMAGE_PATH = Path("input.jpg")
GENERATE_OPTIONS = {"temperature": 0}
PROMPTS = {
	"Free OCR (plain text)": "<image>\nFree OCR.",
	"Document -> Markdown": "<image>\n<|grounding|>Convert the document to markdown.",
	"Deep Parsing (chart / chemical / geometry)": "<image>\nParse the figure.",
	"Multilingual Document": "<image>\nFree OCR.",
	"Image Caption": "<image>\nDescribe this image in detail.",
	"Object Detection": "<image>\nIdentify all objects in the image and output them in bounding boxes.",
}


class DeepSeekOCREngine:
	def __init__(self):
		self.client = Client(host=OLLAMA_HOST)
		self.model = MODEL_NAME

	def check_connection(self):
		"""Check that Ollama is reachable and the configured model is available."""
		try:
			models = self.client.list()
			model_names = [model.model for model in models.models]
			if not any(name == self.model or name.startswith(f"{self.model}:")
					for name in model_names):
				return f"Error: model '{self.model}' is not available"
			return f"Ollama is ready with model: {self.model}"
		except Exception as exc:
			return f"Error: {exc}"

	def extract_text(self, image_path, mode="Free OCR (plain text)", query=""):
		"""Load an image and run the configured DeepSeek-OCR model."""
		prompt = PROMPTS[mode]
		if mode == "Grounding (locate object)":
			prompt = f"<image>\nLocate <|ref|>{query}<|/ref|> in the image."
		elif mode == "Custom Prompt":
			prompt = query if query.startswith("<image>") else f"<image>\n{query}"

		with Image.open(image_path) as image:
			buffer = io.BytesIO()
			image.save(buffer, format="PNG")
			response = self.client.generate(
				model=self.model,
				prompt=prompt,
				images=[buffer.getvalue()],
				options=GENERATE_OPTIONS,
			)
		return response["response"]


def main(image_path, mode="Free OCR (plain text)", query=""):
	engine = DeepSeekOCREngine()

	try:
		text = engine.extract_text(image_path, mode, query)
	except FileNotFoundError:
		print(f"Error: image not found: {image_path}", file=sys.stderr)
		return 2
	except (UnidentifiedImageError, OSError) as exc:
		print(f"Error: cannot read image '{image_path}': {exc}", file=sys.stderr)
		return 2
	except Exception as exc:
		print(f"Error: Ollama request failed: {exc}", file=sys.stderr)
		return 1

	print(text)
	return 0


if __name__ == "__main__":
	raise SystemExit(main(IMAGE_PATH))
