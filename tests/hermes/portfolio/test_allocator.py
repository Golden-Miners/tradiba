from tradiba.hermes.portfolio.allocator.dynamic_allocator import DynamicAllocator

def test_fixed_allocation():
    allocator = DynamicAllocator({"allocation_type": "fixed"})
    strategies = [{"id": "s1"}, {"id": "s2"}]
    allocations = allocator.allocate(strategies, "bull")
    assert allocations["s1"] == 0.5
    assert allocations["s2"] == 0.5

def test_kelly_allocation():
    allocator = DynamicAllocator({"allocation_type": "kelly"})
    strategies = [
        {"id": "s1", "win_rate": 0.6, "win_loss_ratio": 2.0},
        {"id": "s2", "win_rate": 0.4, "win_loss_ratio": 1.5}
    ]
    allocations = allocator.allocate(strategies, "bull")
    # K1 = 0.6 - (0.4 / 2.0) = 0.4. Half kelly = 0.2
    # K2 = 0.4 - (0.6 / 1.5) = 0.0. Half kelly = 0.0
    assert abs(allocations["s1"] - 0.2) < 0.01
    assert abs(allocations["s2"] - 0.0) < 0.01

def test_risk_parity_allocation():
    allocator = DynamicAllocator({"allocation_type": "risk-parity"})
    strategies = [
        {"id": "s1", "volatility": 0.1},
        {"id": "s2", "volatility": 0.2}
    ]
    allocations = allocator.allocate(strategies, "bull")
    # Inv vols: s1 = 10, s2 = 5. Total = 15.
    # s1 = 10/15 = 2/3, s2 = 5/15 = 1/3
    assert abs(allocations["s1"] - 0.666) < 0.01
    assert abs(allocations["s2"] - 0.333) < 0.01
