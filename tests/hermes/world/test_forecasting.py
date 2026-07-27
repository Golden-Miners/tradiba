from tradiba.hermes.world.forecasting.goals import GoalForecaster

def test_goal_forecasting():
    forecaster = GoalForecaster()
    
    result = forecaster.forecast_goal({"id": "g1"}, {})
    assert result["goal_id"] == "g1"
    assert "probability_of_success" in result
