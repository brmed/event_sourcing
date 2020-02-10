from event_sourcing.models import (
    EventStore as EventStoreModel,
    Event as EventModel,
)

from event_sourcing.factories import EventStoreFactory


class EventStoreRepository:
    event_store_model = EventStoreModel
    event_model = EventModel
    factory = EventStoreFactory()

    def save_event(self, event, tracked_object):
        event_store = self.get_event_store(tracked_object)

        self.event_model.stored.create(
            event_store_id=event_store.id,
            name=event.name,
            user_id=event.user.id,
            date=event.date,
            diff=event.diff,
            state=event.state,
        )

        return event

    def get_last_event(self, tracked_object):
        try:
            return self.factory.build_event_from_model(
                self.event_model.stored.filter(
                    event_store__tracked_object_id=tracked_object.object_id,
                    event_store__module=tracked_object.module,
                    event_store__signature=tracked_object.signature
                ).latest('created_at')
            )
        except self.event_model.DoesNotExist:
            return None

    def get_event_store(self, tracked_object):
        event_store, created = self.event_store_model.stored.prefetch_related(
            'event_set',
        ).get_or_create(
            tracked_object_id=tracked_object.object_id,
            module=tracked_object.module,
            signature=tracked_object.signature
        )

        return self.factory.build_from_model(event_store)
