from tradiba.modelops.experiments.tracker import ExperimentTracker

def test_experiments():
    tracker = ExperimentTracker()
    assert tracker.track_experiment("e1", {})
