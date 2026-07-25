import json
import logging
import io

from tradiba.observability.logging import JSONFormatter
from tradiba.observability.metrics import (
    ticks_received_total,
    candles_completed_total
)
from tradiba.observability.tracing import get_tracer
from tradiba.observability.health import HealthManager, HealthCheck, HealthStatus
from tradiba.observability.diagnostics import DiagnosticsCollector
from tradiba.observability.alerts import (
    AlertManager,
    MemoryUsageAlert,
    QueueBacklogAlert,
    AlertNotifier
)
from tradiba.observability.configuration import ConfigValidator, ConfigurationError

import pytest


def test_structured_logging():
    # Capture log output
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JSONFormatter())
    
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    logger.info("Test message", extra={"symbol": "EURUSD", "strategy": "RSI"})
    
    log_str = stream.getvalue()
    log_dict = json.loads(log_str)
    
    assert log_dict["level"] == "INFO"
    assert log_dict["message"] == "Test message"
    assert log_dict["symbol"] == "EURUSD"
    assert log_dict["strategy"] == "RSI"
    assert "timestamp" in log_dict
    
    logger.removeHandler(handler)


def test_metrics_increment():
    initial_ticks = ticks_received_total._value.get()
    initial_candles = candles_completed_total._value.get()
    
    ticks_received_total.inc(5)
    candles_completed_total.inc(1)
    
    assert ticks_received_total._value.get() == initial_ticks + 5
    assert candles_completed_total._value.get() == initial_candles + 1


def test_tracing_span_creation():
    tracer = get_tracer(__name__)
    
    with tracer.start_as_current_span("test.span") as span:
        span.set_attribute("test_attr", "value")
        assert span.is_recording()


class MockDatabaseCheck(HealthCheck):
    @property
    def name(self) -> str:
        return "Database"
        
    def check(self) -> HealthStatus:
        return HealthStatus(name=self.name, healthy=True)


class MockFailingCheck(HealthCheck):
    @property
    def name(self) -> str:
        return "FailingDependency"
        
    def check(self) -> HealthStatus:
        return HealthStatus(name=self.name, healthy=False, message="Timeout")


def test_health_manager():
    hm = HealthManager()
    
    assert hm.is_alive() is True
    
    hm.register(MockDatabaseCheck())
    assert hm.is_ready() is True
    
    hm.register(MockFailingCheck())
    assert hm.is_ready() is False
    
    status = hm.get_status()
    assert status["Database"]["healthy"] is True
    assert status["FailingDependency"]["healthy"] is False


def test_diagnostics_snapshot():
    collector = DiagnosticsCollector()
    collector.queue_depth_func = lambda: 150
    collector.open_positions_func = lambda: 3
    
    diag = collector.snapshot()
    
    assert diag.uptime >= 0
    assert diag.active_threads > 0
    assert diag.memory_usage_mb > 0
    assert diag.open_positions == 3
    assert diag.queue_depth == 150


class MockNotifier(AlertNotifier):
    def __init__(self):
        self.messages = []
        
    def send(self, message: str) -> None:
        self.messages.append(message)


def test_alerts_framework():
    manager = AlertManager()
    notifier = MockNotifier()
    
    manager.add_notifier(notifier)
    manager.add_rule(MemoryUsageAlert(limit_mb=50.0))
    manager.add_rule(QueueBacklogAlert(limit=100))
    
    collector = DiagnosticsCollector()
    # Force mock memory and queue depth
    
    diag = collector.snapshot()
    # Patch the immutable dataclass instance
    from dataclasses import replace
    diag = replace(diag, memory_usage_mb=100.0, queue_depth=200)
    
    manager.run_checks(diag)
    
    assert len(notifier.messages) == 2
    assert "High Memory Usage" in notifier.messages[0]
    assert "Event Queue Backlog" in notifier.messages[1]


def test_configuration_validator(monkeypatch):
    monkeypatch.setenv("TRADIBA_RISK_PCT", "5.0")
    # Should not raise
    ConfigValidator.validate()
    
    monkeypatch.setenv("TRADIBA_RISK_PCT", "15.0")
    with pytest.raises(ConfigurationError):
        ConfigValidator.validate()
