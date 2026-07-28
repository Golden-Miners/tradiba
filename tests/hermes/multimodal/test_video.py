from tradiba.hermes.multimodal.video.intelligence import VideoIntelligence

def test_video():
    vi = VideoIntelligence()
    assert len(vi.segment_scenes("vid.mp4")) == 1
    assert len(vi.extract_keyframes("vid.mp4")) == 2
