# tracing.py
# Distributed Tracing for Nova

import json
import time
import threading
import uuid
from contextvars import ContextVar

trace_id_var = ContextVar('trace_id', default=None)
span_id_var = ContextVar('span_id', default=None)

class Tracer:
    """Distributed tracing system"""
    
    def __init__(self):
        self.spans = {}
        self._lock = threading.Lock()
    
    def start_span(self, name, parent_trace_id=None):
        """Start a new trace span"""
        trace_id = parent_trace_id or str(uuid.uuid4())
        span_id = str(uuid.uuid4())
        
        span = {
            'trace_id': trace_id,
            'span_id': span_id,
            'parent_id': span_id_var.get(),
            'name': name,
            'start_time': time.time(),
            'end_time': None,
            'tags': {}
        }
        
        with self._lock:
            self.spans[span_id] = span
        
        # Set context
        trace_id_var.set(trace_id)
        span_id_var.set(span_id)
        
        return span
    
    def finish_span(self, span_id):
        """Finish a trace span"""
        with self._lock:
            if span_id in self.spans:
                self.spans[span_id]['end_time'] = time.time()
    
    def add_tag(self, span_id, key, value):
        """Add a tag to a span"""
        with self._lock:
            if span_id in self.spans:
                self.spans[span_id]['tags'][key] = value
    
    def get_traces(self):
        """Get all traces"""
        return list(self.spans.values())