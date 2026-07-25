import json
import logging
import sys
from datetime import datetime
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """
    Formatter that outputs logs as JSON strings.
    Converts standard logging fields to structured payload.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        
        
        # Merge extra fields
        standard_fields = {
            'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
            'funcName', 'levelname', 'levelno', 'lineno', 'module',
            'msecs', 'message', 'msg', 'name', 'pathname', 'process',
            'processName', 'relativeCreated', 'stack_info', 'thread', 'threadName', 'taskName'
        }
        for key, value in record.__dict__.items():
            if key not in standard_fields and key != 'extra':
                log_data[key] = value
                
        if hasattr(record, "extra") and isinstance(record.extra, dict): # type: ignore
            log_data.update(record.extra) # type: ignore
            
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_data)


class LoggerFactory:
    """
    Creates and configures loggers that output structured JSON.
    """
    
    _configured = False
    
    @classmethod
    def setup(cls) -> None:
        if cls._configured:
            return
            
        root = logging.getLogger()
        root.setLevel(logging.INFO)
        
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        
        # Remove existing handlers
        for h in root.handlers[:]:
            root.removeHandler(h)
            
        root.addHandler(handler)
        cls._configured = True

    @staticmethod
    def create(name: str) -> logging.Logger:
        LoggerFactory.setup()
        logger = logging.getLogger(name)
        return logger
