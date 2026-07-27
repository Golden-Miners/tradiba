from tradiba.ai.prompts.management import PromptPlatform

def test_prompts():
    plat = PromptPlatform()
    plat.register_prompt("welcome", "Hello {name}", "1.0")
    rendered = plat.render("welcome", {"name": "Alice"})
    assert rendered == "Hello Alice"
