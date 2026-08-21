import time
import threading
import psutil
import pynvml
import torch

class ComputeMonitor:
    def __init__(self, interval=0.2):
        """
        interval: Time in seconds between hardware samples. 
                  0.2s (200ms) is ideal for a ~2-minute script.
        """
        self.interval = interval
        self.running = False
        self.cpu_log = []
        self.gpu_log = []
        
        # Detect NVIDIA GPUs via NVML
        try:
            pynvml.nvmlInit()
            self.gpu_count = pynvml.nvmlDeviceGetCount()
            self.gpu_handles = [pynvml.nvmlDeviceGetHandleByIndex(i) for i in range(self.gpu_count)]
        except Exception:
            self.gpu_count = 0
            print("No NVIDIA GPU/NVML driver detected. Tracking CPU only.")

    def __enter__(self):
        # Flush and synchronize pending GPU workloads before starting clock
        if self.gpu_count > 0 and torch.cuda.is_available():
            torch.cuda.synchronize()

        self.running = True
        self.cpu_log.clear()
        self.gpu_log.clear()
        
        # Run the polling loop in a low-priority background thread
        self.thread = threading.Thread(target=self._poll_utilization, daemon=True)
        self.thread.start()
        self.start_time = time.time()
        return self

    def _poll_utilization(self):
        while self.running:
            # Capture total system CPU usage (all cores combined)
            self.cpu_log.append(psutil.cpu_percent(interval=None))
            
            # Capture utilization across all active GPUs
            if self.gpu_count > 0:
                gpu_samples = []
                for handle in self.gpu_handles:
                    try:
                        util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                        gpu_samples.append(util.gpu)  # Core compute percentage
                    except Exception:
                        gpu_samples.append(0)
                self.gpu_log.append(gpu_samples)
                
            time.sleep(self.interval)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Force block to wait until GPU finishes all computing jobs
        if self.gpu_count > 0 and torch.cuda.is_available():
            torch.cuda.synchronize()
            
        self.running = False
        self.thread.join()
        elapsed = time.time() - self.start_time
        
        if self.gpu_count > 0:
            try: pynvml.nvmlShutdown()
            except: pass

        # Compile Statistics
        self.summary = {"elapsed_seconds": elapsed}

        if self.cpu_log:
            self.summary["cpu_avg"] = sum(self.cpu_log) / len(self.cpu_log)
            self.summary["cpu_max"] = max(self.cpu_log)

        if self.gpu_count > 0 and self.gpu_log:
            # Transpose logs to calculate metrics per individual GPU card
            gpu_avg, gpu_max = [], []
            for idx in range(self.gpu_count):
                device_samples = [sample[idx] for sample in self.gpu_log]
                gpu_avg.append(sum(device_samples) / len(device_samples))
                gpu_max.append(max(device_samples))
            self.summary["gpu_avg"] = gpu_avg
            self.summary["gpu_max"] = gpu_max