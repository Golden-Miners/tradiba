from tradiba.aiops.summarizer import EventSummarizer

def test_summarizer_empty():
    summarizer = EventSummarizer()
    assert "No events" in summarizer.summarize([])

def test_summarizer_events():
    summarizer = EventSummarizer()
    events = [
        {"type": "risk_limit", "strategy_id": "alpha"},
        {"type": "latency_spike", "increase_ms": 120}
    ]
    summary = summarizer.summarize(events)
    assert "Strategy alpha paused" in summary
    assert "latency increased by 120" in summary
