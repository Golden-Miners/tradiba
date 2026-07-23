from tradiba.events import EventBus


class LiveEngine:

    def __init__(
        self,
        event_bus: EventBus,
    ):
        self.event_bus = event_bus

    def run(self):
        pass
