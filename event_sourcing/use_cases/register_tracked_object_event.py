from event_sourcing.repositories import EventStoreRepository
from event_sourcing.factories import EventStoreFactory
from django.utils import timezone

from event_sourcing.domain import TrackedObject


class RegisterTrackedObjectEvent:
    def __init__(self, repository=None, factory=None):
        self.repository = repository or EventStoreRepository()
        self.factory = factory or EventStoreFactory()

    def execute(self, tracked_object, user, *args, **kwargs):
        if not isinstance(tracked_object, TrackedObject):
            raise TypeError('Object is not an instance of TrackedObject')

        current_event = self.factory.build_event_from_tracked_object(
            tracked_object=tracked_object,
            user=user,
            name=kwargs.get('event_name', 'Unknown Event'),
            date=kwargs.get('event_date', timezone.now()),
        )

        last_event = self.repository.get_last_event(tracked_object)

        if last_event:
            current_event.set_diff(last_event)

        self.repository.save_event(current_event, tracked_object)
