from tradiba.ai.factory.synthetic.generator import SyntheticDataPlatform

def test_synthetic():
    generator = SyntheticDataPlatform()
    v = generator.generate_dataset("market_anomalies", "flash_crash", 10)
    data = generator.get_dataset(v)
    assert len(data) == 10
    assert data[0]["scenario"] == "flash_crash"
