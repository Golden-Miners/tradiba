from tradiba.notifications.rules import RuleEngine, AutomationRule, RuleCondition

def test_automation_rules():
    engine = RuleEngine()
    
    # Track execution
    executed = []
    def mock_action(data):
        executed.append(data["id"])
        
    rule = AutomationRule(
        name="High Confidence Signal",
        conditions=[
            RuleCondition(field="type", operator="==", value="signal"),
            RuleCondition(field="confidence", operator=">", value=90)
        ],
        action=mock_action
    )
    engine.add_rule(rule)
    
    # Should not trigger
    engine.process_event({"id": "e1", "type": "signal", "confidence": 85})
    assert len(executed) == 0
    
    # Should trigger
    engine.process_event({"id": "e2", "type": "signal", "confidence": 95})
    assert len(executed) == 1
    assert executed[0] == "e2"
