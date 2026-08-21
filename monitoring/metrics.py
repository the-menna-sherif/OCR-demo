from dataclasses import dataclass, field
from typing import List, Optional

from monitoring.time import OCRTimer
from monitoring.compute_util import ComputeMonitor

import warnings

# Filter out deprecation warnings
warnings.filterwarnings("ignore", category=FutureWarning, message=".* package is deprecated.*")


@dataclass
class OCRMetrics:
    engine_name: str
    image_title: str
    elapsed_seconds: float
    cpu_avg_percent: Optional[float] = None
    cpu_max_percent: Optional[float] = None
    gpu_avg_percent: List[float] = field(default_factory=list)
    gpu_max_percent: List[float] = field(default_factory=list)

    def report(self) -> str:
        lines = [f"{self.engine_name} processed {self.image_title} in {self.elapsed_seconds:.3f}s"]
        if self.cpu_avg_percent is not None:
            lines.append(f"CPU Util -> Avg: {self.cpu_avg_percent:.1f}% | Max: {self.cpu_max_percent:.1f}%")
        for idx, (avg_g, max_g) in enumerate(zip(self.gpu_avg_percent, self.gpu_max_percent)):
            lines.append(f"GPU {idx} Util -> Avg: {avg_g:.1f}% | Max: {max_g:.1f}%")
        return "\n".join(lines)


class MetricsCollector:
    """Single entry point for collecting all monitoring metrics (timing + compute utilization) for one OCR run."""

    def __init__(self, engine, image_path, poll_interval=0.2):
        self.image_path = image_path
        self._timer = OCRTimer(engine)
        self._compute_monitor = ComputeMonitor(interval=poll_interval)
        self.result: Optional[OCRMetrics] = None

    def __enter__(self):
        self._compute_monitor.__enter__()
        self._timer.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        timing = self._timer.stop(self.image_path)
        self._compute_monitor.__exit__(exc_type, exc_val, exc_tb)
        summary = self._compute_monitor.summary

        self.result = OCRMetrics(
            engine_name=timing.engine_name,
            image_title=timing.image_title,
            elapsed_seconds=timing.elapsed_seconds,
            cpu_avg_percent=summary.get("cpu_avg"),
            cpu_max_percent=summary.get("cpu_max"),
            gpu_avg_percent=summary.get("gpu_avg", []),
            gpu_max_percent=summary.get("gpu_max", []),
        )
        return False
