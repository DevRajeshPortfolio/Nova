# metrics.py
# Metrics Collection for Nova

import time
import threading
from collections import defaultdict

class MetricsCollector:
    """Metrics collection system"""
    
    def __init__(self):
        self.counters = defaultdict(int)
        self.gauges = defaultdict(float)
        self.histograms = defaultdict(list)
        self.timers = defaultdict(list)
        self._lock = threading.Lock()
    
    def increment(self, name, value=1):
        """Increment a counter"""
        with self._lock:
            self.counters[name] += value
    
    def gauge(self, name, value):
        """Set a gauge value"""
        with self._lock:
            self.gauges[name] = value
    
    def histogram(self, name, value):
        """Record a histogram value"""
        with self._lock:
            self.histograms[name].append(value)
            # Keep only last 1000 values
            if len(self.histograms[name]) > 1000:
                self.histograms[name] = self.histograms[name][-1000:]
    
    def timer(self, name):
        """Time a function"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                start = time.time()
                result = func(*args, **kwargs)
                duration = time.time() - start
                self.histogram(name, duration)
                return result
            return wrapper
        return decorator
    
    def get_metrics(self):
        """Get all metrics"""
        with self._lock:
            return {
                'counters': dict(self.counters),
                'gauges': dict(self.gauges),
                'histograms': {
                    k: {
                        'min': min(v) if v else 0,
                        'max': max(v) if v else 0,
                        'avg': sum(v) / len(v) if v else 0,
                        'count': len(v)
                    }
                    for k, v in self.histograms.items()
                },
                'timers': {
                    k: {
                        'min': min(v) if v else 0,
                        'max': max(v) if v else 0,
                        'avg': sum(v) / len(v) if v else 0,
                        'count': len(v)
                    }
                    for k, v in self.timers.items()
                }
            }