from tradiba.data_mesh.streaming.platform import StreamingPlatform

def test_streaming():
    plat = StreamingPlatform()
    assert plat.start_pipeline("pipe1")
