import time
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TimingResult:
    engine_name: str
    image_title: str
    elapsed_seconds: float


class OCRTimer:
    def __init__(self, engine):
        self.engine = engine
        self._start = None

    def start(self):
        if self._start is not None:
            raise RuntimeError("start() called without a matching stop()")
        self._start = time.perf_counter() # starts the timer

    def stop(self, image_path):
        if self._start is None:
            raise RuntimeError("stop() called without a preceding start()")
        elapsed = time.perf_counter() - self._start # calculates the elapsed time
        self._start = None
        return TimingResult(
            engine_name=self.engine.__class__.__name__,
            image_title=Path(image_path).name,
            elapsed_seconds=elapsed,
        )

def main():
    # Example usage of OCRTimer with a dummy engine
    class DummyEngine:
        def extract_text(self, image_path):
            time.sleep(1)  # Simulate some processing time
            return "Dummy text"

    engine = DummyEngine()
    timer = OCRTimer(engine)

    image_path = "dummy_image.jpg"
    timer.start()
    text = engine.extract_text(image_path)
    timing_result = timer.stop(image_path)

    print(f"Extracted text: {text}")
    print(f"{timing_result.engine_name} processed {timing_result.image_title} in {timing_result.elapsed_seconds:.3f}s")
