from tradiba.hermes.research.planner.research_planner import ResearchPlanner, ResearchTopic

def test_research_planner_prioritization():
    planner = ResearchPlanner()
    planner.backlog.append(ResearchTopic(id="1", description="Low priority", priority=2))
    planner.backlog.append(ResearchTopic(id="2", description="High priority", priority=1))
    
    next_topic = planner.get_next_topic()
    assert next_topic is not None
    assert next_topic.id == "2"
    assert next_topic.status == "in_progress"
