from tradiba.hermes.innovation.generators.skill_generator import SkillGenerator

def test_skill_generation():
    gen = SkillGenerator()
    skill = gen.generate_skill({"description": "News Sentiment Analyzer"})
    
    assert skill["name"] == "News"
    assert "data:read" in skill["required_permissions"]
    assert "execute" in skill["code"]
