import os
import time
import logging
import psutil
from functools import wraps
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
logger = logging.getLogger("performance")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    os.path.join(LOG_DIR, "performance.log"),
    maxBytes=5_000_000,
    backupCount=3
)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

_PROCESS = psutil.Process(os.getpid())


def get_app_metrics() -> dict:
    """Metrics for current Python process"""
    mem = _PROCESS.memory_info().rss / (1024 ** 2)
    cpu = _PROCESS.cpu_percent(interval=0.5)
    return {
        "app_cpu_percent": cpu,
        "app_ram_mb": round(mem, 2),
    }


# Timing Utilities

def timed(stage_name: str):
    """
    Decorator to measure execution time of pipeline stages
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start

            logger.info(f"{stage_name} | time={elapsed:.3f}s")
            return result
        return wrapper
    return decorator


def measure_block(stage_name: str):
    """
    Context manager timing for inline blocks
    """
    class Timer:
        def __enter__(self):
            self.start = time.perf_counter()

        def __exit__(self):
            elapsed = time.perf_counter() - self.start
            logger.info(f"{stage_name} | time={elapsed:.3f}s")
    return Timer()


# LLM Monitoring

def monitor_llm_call(fn):
    """
    Decorator for LLM inference timing
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        response = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start

        logger.info(f"LLM Inference | time={elapsed:.3f}s")
        return response
    return wrapper


# Gradio-Friendly Metrics Output

def format_metrics_markdown() -> str:
    """Formatted markdown for Gradio UI"""
    app = get_app_metrics()

    return f"""

### 🧠 App Metrics
- **Process CPU:** {app['app_cpu_percent']}%
- **Process RAM:** {app['app_ram_mb']} MB
"""