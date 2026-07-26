from engineering.releases.release_checklist import run_release_checklist

def test_release_checklist():
    """Verify the release checklist executes and returns expected status."""
    result = run_release_checklist()
    assert result is True, "Release checklist failed when it should pass"
