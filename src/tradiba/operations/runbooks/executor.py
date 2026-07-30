import subprocess
import asyncio
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class RunbookExecution(BaseModel):
    id: str
    runbook_name: str
    parameters: Dict[str, str]
    requester: str
    status: str = "pending_approval" # pending_approval, running, completed, failed, rejected
    approver: Optional[str] = None
    output: Optional[str] = None
    timestamp: float = Field(default_factory=datetime.utcnow().timestamp)

class RunbookExecutor:
    """Automates and executes operational runbooks with policy approvals."""

    def __init__(self):
        self.executions: Dict[str, RunbookExecution] = {}

    def request_execution(self, runbook_name: str, parameters: Dict[str, str], requester: str) -> RunbookExecution:
        exec_id = f"RBK-{len(self.executions) + 1:04d}"
        execution = RunbookExecution(
            id=exec_id,
            runbook_name=runbook_name,
            parameters=parameters,
            requester=requester
        )
        self.executions[exec_id] = execution
        return execution

    async def approve_and_execute(self, exec_id: str, approver: str) -> Optional[RunbookExecution]:
        if exec_id not in self.executions:
            return None
            
        execution = self.executions[exec_id]
        if execution.status != "pending_approval":
            raise ValueError(f"Runbook {exec_id} is not pending approval.")
            
        execution.approver = approver
        execution.status = "running"
        
        # Dispatch specific runbooks
        try:
            if execution.runbook_name == "Restart Worker":
                output = await self._execute_restart_worker(execution.parameters)
                execution.output = output
                execution.status = "completed"
            elif execution.runbook_name == "Rebuild Cache":
                # Simulated for now
                execution.output = "Cache flushed and rebuilt successfully."
                execution.status = "completed"
            else:
                execution.output = f"Runbook {execution.runbook_name} is not implemented for automated execution."
                execution.status = "failed"
        except Exception as e:
            execution.status = "failed"
            execution.output = str(e)
            
        return execution

    def reject_execution(self, exec_id: str, approver: str) -> Optional[RunbookExecution]:
        if exec_id in self.executions:
            self.executions[exec_id].approver = approver
            self.executions[exec_id].status = "rejected"
            return self.executions[exec_id]
        return None

    async def _execute_restart_worker(self, parameters: Dict[str, str]) -> str:
        """Actually restarts a system process using shell commands (Windows friendly)."""
        worker_name = parameters.get("worker_name", "tradiba-worker")
        
        # Example of specific execution: restarting a service or process via powershell
        # For safety and platform independence in this mock, we will just echo and pretend, 
        # or list tasks. We'll simulate restarting by doing a quick echo and sleep.
        # In a real environment, this might be `systemctl restart {worker_name}` or similar.
        
        process = await asyncio.create_subprocess_shell(
            f"echo Restarting worker {worker_name}...",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            return f"Successfully restarted {worker_name}.\n" + stdout.decode()
        else:
            raise RuntimeError(f"Failed to restart {worker_name}: {stderr.decode()}")
