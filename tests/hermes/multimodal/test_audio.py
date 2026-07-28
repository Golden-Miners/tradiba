from tradiba.hermes.multimodal.audio.intelligence import AudioIntelligence

def test_audio():
    ai = AudioIntelligence()
    assert ai.transcribe(b"audio") == "The market is volatile today."
    assert ai.extract_sentiment("volatile") == "bearish"
    assert len(ai.diarize(b"audio")) == 1
