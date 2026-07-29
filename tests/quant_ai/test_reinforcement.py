from tradiba.quant_ai.reinforcement.research import ReinforcementLearningResearch

def test_reinforcement():
    research = ReinforcementLearningResearch()
    assert research.train_policy("env_1") == "policy_for_env_1"
