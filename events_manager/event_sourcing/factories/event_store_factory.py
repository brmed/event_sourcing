from events_manager.event_sourcing.domain import (
    EventStore,
    Event,
    TrackedObject,
)

from django.contrib.auth.models import User


class EventStoreFactory:
    event_store_domain = EventStore
    event_domain = Event
    tracked_object_domain = TrackedObject

    def build_from_model(self, event_store_model):
        attributes = {}

        attributes['events'] = [
            self.build_event_from_model(e)
            for e in event_store_model.events()
        ]

        attributes['tracked_object'] = self.tracked_object_domain(
            object_id=event_store_model.tracked_object_id,
            module=event_store_model.module,
            signature=event_store_model.signature,
        )

        attributes['id'] = event_store_model.id

        return self.event_store_domain(**attributes)

    def build_event_from_tracked_object(self, tracked_object, *args, **kwargs):
        return self.event_domain(
            name=kwargs['name'],
            date=kwargs['date'],
            user=kwargs['user'],
            state=tracked_object.get_state(),
        )

    def build_event_from_model(self, event_model):
        attributes = {}

        attributes['name'] = event_model.name
        attributes['date'] = event_model.date
        attributes['user'] = User(
            username = event_model.user.username,
            email = event_model.user.email,
            first_name = event_model.user.first_name,
            last_name = event_model.user.last_name,
            id = event_model.user.id
        )
        attributes['state'] = event_model.state
        attributes['diff'] = event_model.diff

        return self.event_domain(**attributes)
