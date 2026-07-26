from tradiba.control_plane.configuration import HierarchicalConfig, ConfigurationNode

def test_configuration_inheritance():
    cfg = HierarchicalConfig(
        global_cfg=ConfigurationNode({"log_level": "INFO", "timeout": 30}),
        environment_cfg=ConfigurationNode({"timeout": 60, "env": "prod"}),
        cluster_cfg=ConfigurationNode({"cluster_id": "c1"}),
        node_cfg=ConfigurationNode({"log_level": "DEBUG"})
    )
    
    # Node overrides global
    assert cfg.resolve("log_level") == "DEBUG"
    # Environment overrides global
    assert cfg.resolve("timeout") == 60
    # Fallback to global
    assert cfg.resolve("missing", "default") == "default"
    # Cluster specific
    assert cfg.resolve("cluster_id") == "c1"
