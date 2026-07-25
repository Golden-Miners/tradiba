from typing import Literal
from pydantic import BaseModel, Field

class PluginManifest(BaseModel):
    name: str = Field(..., description="Unique name of the plugin")
    version: str = Field(..., description="Version of the plugin")
    author: str = Field(..., description="Author of the plugin")
    api_version: str = Field(..., description="Target tradiba SDK API version")
    type: Literal["strategy", "indicator", "broker", "risk"] = Field(
        ..., description="Type of the plugin"
    )
    entrypoint: str = Field(
        ..., description="Python entrypoint string (e.g. module:ClassName)"
    )
    description: str = Field("", description="Optional description")
