from typing import Callable, Any, Dict
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class RuleCondition(BaseModel):
    field: str
    operator: str
    value: Any
    
    def evaluate(self, event_data: Dict[str, Any]) -> bool:
        event_value = event_data.get(self.field)
        if event_value is None:
            return False
            
        if self.operator == "==":
            return event_value == self.value
        if self.operator == ">":
            return event_value > self.value
        if self.operator == "<":
            return event_value < self.value
        if self.operator == ">=":
            return event_value >= self.value
        if self.operator == "<=":
            return event_value <= self.value
        if self.operator == "in":
            return event_value in self.value
        return False

class AutomationRule:
    def __init__(self, name: str, conditions: list[RuleCondition], action: Callable[[Dict[str, Any]], None]):
        self.name = name
        self.conditions = conditions
        self.action = action
        
    def check_and_execute(self, event_data: Dict[str, Any]):
        for condition in self.conditions:
            if not condition.evaluate(event_data):
                return False
                
        logger.info(f"Automation Rule Triggered: {self.name}")
        self.action(event_data)
        return True

class RuleEngine:
    def __init__(self):
        self.rules: list[AutomationRule] = []
        
    def add_rule(self, rule: AutomationRule):
        self.rules.append(rule)
        
    def process_event(self, event_data: Dict[str, Any]):
        triggered = []
        for rule in self.rules:
            if rule.check_and_execute(event_data):
                triggered.append(rule.name)
        return triggered
