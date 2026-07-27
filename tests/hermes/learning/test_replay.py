from tradiba.hermes.learning.replay.engine import ExperienceReplayEngine

def test_experience_replay():
    engine = ExperienceReplayEngine()
    result = engine.replay_session("sess_1", [{"type": "TradeExecuted"}])
    assert result["events_replayed"] == 1
    assert result["status"] == "COMPLETED"
