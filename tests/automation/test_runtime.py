from tradiba.automation.runtime.execution_context import ExecutionContext

def test_runtime():
    ctx = ExecutionContext()
    ctx.inject_secrets({"key": "val"})
    assert ctx.context["secrets"]["key"] == "val"
    ctx.save_checkpoint({"step": 1})
    assert ctx.context["checkpoint"]["step"] == 1
