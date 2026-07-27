from tradiba.hermes.hcos.scheduler.cognitive_scheduler import CognitiveScheduler

def test_scheduler_priority():
    scheduler = CognitiveScheduler()
    scheduler.schedule_task("t1", 5, {})
    scheduler.schedule_task("t2", 1, {})
    
    first = scheduler.next_task()
    assert first["task_id"] == "t2"
    
    second = scheduler.next_task()
    assert second["task_id"] == "t1"

def test_scheduler_preempt():
    scheduler = CognitiveScheduler()
    scheduler.schedule_task("t1", 5, {})
    scheduler.preempt_critical("CRITICAL", {})
    
    first = scheduler.next_task()
    assert first["task_id"] == "CRITICAL"
    assert first["priority"] == 0
