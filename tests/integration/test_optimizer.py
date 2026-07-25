import csv
import os
import tempfile

from tradiba.optimization.configuration import OptimizationConfig, Parameter
from tradiba.optimization.engine import OptimizationEngine
from tradiba.optimization.ranking import ObjectiveRankingStrategy
from tradiba.optimization.search.grid import GridSearch
from tradiba.optimization.search.random import RandomSearch
from tradiba.optimization.walk_forward import WalkForwardOptimizer
from tradiba.optimization.monte_carlo import MonteCarloEngine
from tradiba.market.models import Timeframe


def _create_dummy_csv(path: str):
    with open(path, 'w', newline='') as csvfile:
        fieldnames = ['time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
            'time': '2026-07-25T12:00:00',
            'open': 1.1000,
            'high': 1.1020,
            'low': 1.0990,
            'close': 1.1010,
            'tick_volume': 100,
            'spread': 1,
            'real_volume': 100
        })
        writer.writerow({
            'time': '2026-07-25T12:01:00',
            'open': 1.1010,
            'high': 1.1030,
            'low': 1.1000,
            'close': 1.1020,
            'tick_volume': 100,
            'spread': 1,
            'real_volume': 100
        })


def test_grid_search():
    params = [
        Parameter("tp", 10.0, 30.0, 10.0),
        Parameter("sl", 5.0, 15.0, 5.0)
    ]
    search = GridSearch(params)
    results = list(search.generate())
    
    # tp: 10, 20, 30 (3)
    # sl: 5, 10, 15 (3)
    # Total combinations = 3 * 3 = 9
    assert len(results) == 9
    assert {"tp": 10.0, "sl": 5.0} in results


def test_random_search():
    params = [
        Parameter("risk", 1.0, 5.0, 0.5)
    ]
    # step 0.5 -> 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0 (9 steps)
    search1 = RandomSearch(params, seed=42, max_iterations=10)
    res1 = list(search1.generate())
    
    search2 = RandomSearch(params, seed=42, max_iterations=10)
    res2 = list(search2.generate())
    
    # Seeds match, so results should match exactly
    assert res1 == res2
    assert len(res1) == 10
    
    search3 = RandomSearch(params, seed=99, max_iterations=10)
    res3 = list(search3.generate())
    
    # Different seed, so results should differ
    assert res1 != res3


def test_optimization_engine():
    # Use a dummy CSV for backtest engine feed
    fd, path = tempfile.mkstemp(suffix=".csv")
    os.close(fd)
    
    try:
        _create_dummy_csv(path)
        
        config = OptimizationConfig(
            workers=2,
            max_iterations=4, # limit combinations
            random_seed=42,
            objective="net_profit",
            walk_forward_windows=2
        )
        
        params = [
            Parameter("risk", 1.0, 5.0, 1.0)
        ]
        search = GridSearch(params)
        ranking = ObjectiveRankingStrategy(objective_field="net_profit")
        engine = OptimizationEngine(config=config, ranking_strategy=ranking)
        
        results = engine.optimize(search, data_file=path, symbol="EURUSD", timeframe=Timeframe.M1)
        
        assert len(results) == 4 # Max iterations limited to 4
        # Since it's a simulated run with PaperExecutionAdapter not placing dummy trades independently,
        # net profit should be 0, but the pipeline works.
        assert results[0].statistics.net_profit == 0.0
        
    finally:
        os.remove(path)


def test_monte_carlo():
    mc = MonteCarloEngine(seed=42)
    # Example: 3 wins, 2 losses
    trades = [100.0, 150.0, -50.0, -100.0, 200.0]
    
    res1 = mc.simulate(trades, iterations=500)
    assert res1["iterations"] == 500
    assert "average_max_drawdown" in res1
    assert "worst_case_drawdown" in res1
    
    mc2 = MonteCarloEngine(seed=42)
    res2 = mc2.simulate(trades, iterations=500)
    
    assert res1 == res2


def test_walk_forward():
    fd, path = tempfile.mkstemp(suffix=".csv")
    os.close(fd)
    
    try:
        _create_dummy_csv(path)
        
        config = OptimizationConfig(
            workers=1,
            max_iterations=2,
            random_seed=42,
            objective="net_profit",
            walk_forward_windows=2
        )
        params = [Parameter("risk", 1.0, 2.0, 1.0)]
        
        engine = OptimizationEngine(
            config=config, 
            ranking_strategy=ObjectiveRankingStrategy("net_profit")
        )
        wf = WalkForwardOptimizer(engine=engine)
        
        res = wf.optimize(
            search_algorithm=GridSearch(params),
            data_file=path,
            symbol="EURUSD",
            timeframe=Timeframe.M1,
            windows=2
        )
        
        assert len(res["folds"]) == 2
        assert len(res["overall_oos_results"]) == 2
        
    finally:
        os.remove(path)
