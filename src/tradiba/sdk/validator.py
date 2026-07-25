from typing import Any

from tradiba.sdk.metadata import PluginManifest
from tradiba.sdk.exceptions import PluginValidationError, IncompatibleApiVersionError
from tradiba.sdk.plugin import Plugin

class PluginValidator:
    def __init__(self, platform_api_version: str):
        self.platform_api_version = platform_api_version

    def validate_manifest(self, manifest: PluginManifest) -> None:
        if manifest.api_version != self.platform_api_version:
            # We could do semantic versioning comparison here.
            # For simplicity, exact match or major version match.
            if manifest.api_version.split('.')[0] != self.platform_api_version.split('.')[0]:
                raise IncompatibleApiVersionError(
                    f"Plugin requires API {manifest.api_version}, but platform runs {self.platform_api_version}"
                )

    def validate_instance(self, instance: Any) -> None:
        if not isinstance(instance, Plugin):
            raise PluginValidationError(
                f"Plugin entrypoint must inherit from SDK Plugin class, got {type(instance)}"
            )
