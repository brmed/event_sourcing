import attr
import typing
from events_manager.event_sourcing.domain.tracked_object import TrackedObject
from events_manager.event_sourcing.domain.event import Event


@attr.s(auto_attribs=True, cmp=False, repr=False, kw_only=True)
class EventStore:
    tracked_object: TrackedObject
    events: typing.List[Event] = attr.Factory(list)
    id: int = None

    def get_last_event(self):
        return self.events[-1] if self.events else None
