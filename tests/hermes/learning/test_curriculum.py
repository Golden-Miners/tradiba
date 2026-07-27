from tradiba.hermes.learning.curriculum.scheduler import LearningCurriculum

def test_learning_curriculum():
    scheduler = LearningCurriculum()
    assert scheduler.get_tasks_for_cadence("daily") == "replay_yesterday"
    assert scheduler.get_tasks_for_cadence("yearly") == "NO_TASK"
