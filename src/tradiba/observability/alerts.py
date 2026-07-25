from abc import ABC, abstractmethod
from typing import List

from .diagnostics import RuntimeDiagnostics


class AlertNotifier(ABC):
    """Sink for sending alerts."""
    
    @abstractmethod
    def send(self, message: str) -> None:
        pass


class WebhookNotifier(AlertNotifier):
    """Basic webhook notifier (e.g. for Slack/Discord)."""
    
    def __init__(self, url: str):
        self.url = url
        
    def send(self, message: str) -> None:
        import urllib.request
        import urllib.error
        import json
        
        req = urllib.request.Request(
            self.url,
            data=json.dumps({"text": message}).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        try:
            urllib.request.urlopen(req, timeout=5)
        except urllib.error.URLError:
            # We silently fail here to not crash the main pipeline
            pass


class AlertRule(ABC):
    """Evaluates metrics/diagnostics to trigger alerts."""
    
    @abstractmethod
    def evaluate(self, diagnostics: RuntimeDiagnostics) -> str | None:
        """Returns alert message if triggered, else None."""
        pass


class MemoryUsageAlert(AlertRule):
    """Alerts if memory exceeds limit."""
    
    def __init__(self, limit_mb: float = 1024.0):
        self.limit = limit_mb
        
    def evaluate(self, diagnostics: RuntimeDiagnostics) -> str | None:
        if diagnostics.memory_usage_mb > self.limit:
            return f"High Memory Usage: {diagnostics.memory_usage_mb:.2f} MB exceeds {self.limit} MB."
        return None


class QueueBacklogAlert(AlertRule):
    """Alerts if event queue is backlogged."""
    
    def __init__(self, limit: int = 1000):
        self.limit = limit
        
    def evaluate(self, diagnostics: RuntimeDiagnostics) -> str | None:
        if diagnostics.queue_depth > self.limit:
            return f"Event Queue Backlog: {diagnostics.queue_depth} events."
        return None


class AlertManager:
    """Evaluates rules and routes alerts to notifiers."""
    
    def __init__(self):
        self._rules: List[AlertRule] = []
        self._notifiers: List[AlertNotifier] = []

    def add_rule(self, rule: AlertRule) -> None:
        self._rules.append(rule)
        
    def add_notifier(self, notifier: AlertNotifier) -> None:
        self._notifiers.append(notifier)
        
    def run_checks(self, diagnostics: RuntimeDiagnostics) -> None:
        for rule in self._rules:
            msg = rule.evaluate(diagnostics)
            if msg:
                for notifier in self._notifiers:
                    notifier.send(msg)
