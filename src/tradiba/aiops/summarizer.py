from typing import Any

class EventSummarizer:
    """Summarizes raw platform events into human-readable operations summaries."""
    def summarize(self, events: list[dict[str, Any]]) -> str:
        if not events:
            return "No events detected in the current window."
            
        summary_lines = []
        for event in events:
            event_type = event.get("type")
            if event_type == "risk_limit":
                summary_lines.append(f"• Strategy {event.get('strategy_id', 'unknown')} paused due to risk limit.")
            elif event_type == "latency_spike":
                summary_lines.append(f"• Broker latency increased by {event.get('increase_ms', 0)} ms.")
            elif event_type == "exposure_change":
                summary_lines.append(f"• Portfolio exposure decreased by {event.get('decrease_pct', 0)}%.")
            else:
                summary_lines.append(f"• Unclassified event: {event_type}")
                
        # Simple deduplication or fallback
        if not summary_lines:
            summary_lines.append("• No execution failures detected.")
            
        return "\n".join(summary_lines)
