from dataclasses import dataclass
from pathlib import Path


@dataclass
class TokenResult:
    engine_name: str
    image_title: str
    prompt_tokens: int
    completion_tokens: int
    prompt_eval_seconds: float
    eval_seconds: float

    @property
    def total_tokens(self):
        return self.prompt_tokens + self.completion_tokens


class OllamaTokenCounter:
    def __init__(self, engine):
        self.engine = engine

    def record(self, image_path, response):
        return TokenResult(
            engine_name=self.engine.__class__.__name__,
            image_title=Path(image_path).name,
            prompt_tokens=response.get("prompt_eval_count", 0) or 0,
            completion_tokens=response.get("eval_count", 0) or 0,
            prompt_eval_seconds=(response.get("prompt_eval_duration", 0) or 0) / 1e9,
            eval_seconds=(response.get("eval_duration", 0) or 0) / 1e9,
        )

def main():
    # Example usage of OllamaTokenCounter with a dummy engine
    class DummyEngine:
        def extract_text(self, image_path):
            return {
                "response": "Dummy text",
                "prompt_eval_count": 11,
                "prompt_eval_duration": 13074791,
                "eval_count": 18,
                "eval_duration": 52479709,
            }

    engine = DummyEngine()
    counter = OllamaTokenCounter(engine)

    image_path = "dummy_image.jpg"
    response = engine.extract_text(image_path)
    token_result = counter.record(image_path, response)

    print(f"Extracted text: {response['response']}")
    print(
        f"{token_result.engine_name} processed {token_result.image_title}: "
        f"{token_result.prompt_tokens} input tokens, {token_result.completion_tokens} output tokens "
        f"({token_result.total_tokens} total)"
    )
