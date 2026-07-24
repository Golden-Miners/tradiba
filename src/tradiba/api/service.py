"""
Background service that runs the FastAPI application.
"""

import threading
import uvicorn
import logging
from tradiba.core.service import Service
from tradiba.config.settings import APISettings
from tradiba.core.container import Container

logger = logging.getLogger(__name__)


class APIService(Service):
    """
    Runs the FastAPI application inside a daemon thread using Uvicorn.
    """

    def __init__(self, settings: APISettings, container: Container) -> None:
        self.settings = settings
        self.container = container
        self._thread: threading.Thread | None = None
        self._server: uvicorn.Server | None = None

    def start(self) -> None:
        try:
            from tradiba.api.app import app

            # Inject container into app state so endpoints can query services
            app.state.container = self.container

            # Configure uvicorn
            # Disable signals since we are running in a background thread
            config = uvicorn.Config(
                app=app,
                host=self.settings.host,
                port=self.settings.port,
                log_level="info",
            )
            self._server = uvicorn.Server(config)

            def run_server():
                try:
                    self._server.run()
                except Exception as e:
                    logger.error(f"APIService server crashed: {e}", exc_info=True)

            original_install = getattr(self._server, "install_signal_handlers", None)
            if original_install:
                self._server.install_signal_handlers = lambda *args, **kwargs: None

            self._thread = threading.Thread(target=run_server, daemon=True, name="APIServerThread")
            self._thread.start()
            logger.info(f"APIService starting on {self.settings.host}:{self.settings.port}")
        except Exception as e:
            logger.error(f"Failed to start APIService: {e}", exc_info=True)

    def stop(self) -> None:
        if self._server:
            logger.info("APIService stopping...")
            self._server.should_exit = True
        
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)
            logger.info("APIService stopped.")
