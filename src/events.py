from enum import Enum, auto
from typing import Callable, Dict
import sys


class Event(Enum):
    REFRESH_NETWORKS = auto()


event_subscribers: Dict[Event, list[Callable]] = {}


def emit_event(event: Event, *args):
    if event not in event_subscribers:
        print(f"Event {event} doesn't have any functions subscribed to it.",
              file=sys.stderr)
    for function in event_subscribers[event]:
        function(*args)


def attach_to_event(event: Event, function: Callable):
    if event not in event_subscribers:
        event_subscribers[event] = []
    event_subscribers[event].append(function)
