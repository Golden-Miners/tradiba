from pydantic import BaseModel

class PortfolioResponse(BaseModel):
    equity: float
    balance: float
    margin: float
    profit: float
    free_margin: float

class HealthResponse(BaseModel):
    status: str
    version: str
