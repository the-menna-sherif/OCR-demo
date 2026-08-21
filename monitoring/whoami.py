from dataclasses import dataclass, field
from typing import List

import psutil
import pynvml


@dataclass
class DeviceSpecs:
    cores: int
    ram_gb: float
    gpu_names: List[str] = field(default_factory=list)
    gpu_vram_gb: List[float] = field(default_factory=list)

    def report(self) -> str:
        lines = [
            f"Cores: {self.cores}",
            f"RAM: {self.ram_gb:.1f} GB",
        ]
        if self.gpu_names:
            for idx, (name, vram) in enumerate(zip(self.gpu_names, self.gpu_vram_gb)):
                lines.append(f"GPU {idx}: {name} | VRAM: {vram:.1f} GB")
        else:
            lines.append("GPU: None detected")
        return "\n".join(lines)


def get_device_specs() -> DeviceSpecs:
    cores = psutil.cpu_count(logical=True)
    ram_gb = psutil.virtual_memory().total / (1024 ** 3)

    gpu_names, gpu_vram_gb = [], []
    try:
        pynvml.nvmlInit()
        for i in range(pynvml.nvmlDeviceGetCount()):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            name = pynvml.nvmlDeviceGetName(handle)
            gpu_names.append(name.decode() if isinstance(name, bytes) else name)
            gpu_vram_gb.append(pynvml.nvmlDeviceGetMemoryInfo(handle).total / (1024 ** 3))
        pynvml.nvmlShutdown()
    except Exception:
        pass

    return DeviceSpecs(cores=cores, ram_gb=ram_gb, gpu_names=gpu_names, gpu_vram_gb=gpu_vram_gb)


def main():
    print("*************** device specs *******************")
    print(get_device_specs().report())


if __name__ == "__main__":
    main()
