from uuid import uuid4
from tradiba.research.registry import ModelRegistry, RegisteredModel, ModelStatus

def test_model_promotion():
    registry = ModelRegistry()
    model_id = uuid4()
    
    model = RegisteredModel(model_id, uuid4())
    registry.register(model)
    
    assert registry._models[model_id].status == ModelStatus.CANDIDATE
    
    registry.promote(model_id, ModelStatus.SHADOW, "admin")
    
    promoted = registry._models[model_id]
    assert promoted.status == ModelStatus.SHADOW
    assert promoted.promoted_by == "admin"
    assert promoted.promotion_time is not None
