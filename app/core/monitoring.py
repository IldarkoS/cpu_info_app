import psutil

def collect_system_metrics():
    data = {
        "cpu_times": psutil.cpu_times()._asdict(),
        "cpu_percent": psutil.cpu_percent(interval=None),
        "cpu_frequencies": psutil.cpu_freq().current,
        "memory_percent": psutil.virtual_memory().percent,
        "cpu_stats": psutil.cpu_stats()._asdict(),
        "load_avg": {i: x / psutil.cpu_count() * 100 for i, x in enumerate(psutil.getloadavg(), start=1)},
        "memory_info": psutil.virtual_memory()._asdict(),
        "swap_memory": psutil.swap_memory()._asdict()
    }

    return data