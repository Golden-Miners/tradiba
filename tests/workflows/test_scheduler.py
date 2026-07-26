from datetime import datetime
from tradiba.workflows.scheduler import OperationalScheduler

def test_operational_scheduler():
    scheduler = OperationalScheduler()
    
    context = {"called": False}
    def action():
        context["called"] = True
        
    scheduler.schedule_job("test_job", "* * * * *", action)
    scheduler.run_pending(datetime.now())
    
    assert context["called"] is True
