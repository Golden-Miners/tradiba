import pytest

from tradiba.cqrs import (
    Command,
    CommandDispatcher,
    CommandHandler,
)
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DummyCommand(Command):
    message: str


class DummyCommandHandler(CommandHandler[DummyCommand]):
    def __init__(self):
        self.handled_messages = []

    def handle(self, command: DummyCommand) -> None:
        self.handled_messages.append(command.message)


def test_dispatcher_routing():
    dispatcher = CommandDispatcher()
    handler = DummyCommandHandler()
    dispatcher.register(DummyCommand, handler)

    command = DummyCommand(message="test message")
    dispatcher.dispatch(command)

    assert len(handler.handled_messages) == 1
    assert handler.handled_messages[0] == "test message"


def test_dispatcher_unregistered_command():
    dispatcher = CommandDispatcher()
    command = DummyCommand(message="unhandled")

    with pytest.raises(ValueError, match="No handler registered for command: DummyCommand"):
        dispatcher.dispatch(command)
