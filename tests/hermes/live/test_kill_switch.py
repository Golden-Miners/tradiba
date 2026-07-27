from tradiba.hermes.live.emergency.kill_switch import KillSwitch

def test_kill_switch_global():
    ks = KillSwitch()
    assert not ks.is_killed()
    ks.activate_global()
    assert ks.is_killed()
    ks.deactivate_global()
    assert not ks.is_killed()

def test_kill_switch_scoped():
    ks = KillSwitch()
    assert not ks.is_killed(["tenant:123"])
    
    ks.activate_scoped("tenant:123")
    assert ks.is_killed(["tenant:123"])
    assert not ks.is_killed(["tenant:456"])
    
    ks.deactivate_scoped("tenant:123")
    assert not ks.is_killed(["tenant:123"])
