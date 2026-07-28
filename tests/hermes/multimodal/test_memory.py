from tradiba.hermes.multimodal.memory.multimodal_memory import MultimodalMemory

def test_memory():
    mm = MultimodalMemory()
    mm.store_memory("image", b"img", {"source": "chart1"})
    assert len(mm.retrieve("query")) == 1
