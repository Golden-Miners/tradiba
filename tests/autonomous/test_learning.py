from tradiba.autonomous.learning.continuous import ContinuousEnterpriseLearning

def test_learning():
    learning = ContinuousEnterpriseLearning()
    learning.learn_from_mission("m1", {})
