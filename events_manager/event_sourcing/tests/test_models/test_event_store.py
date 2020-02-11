from django.test import TestCase
from model_mommy import mommy
from event_sourcing.models import EventStore


class EventStoreModelTestCase(TestCase):
    def test_instantiate(self):
        event_store = mommy.make(EventStore)
        self.assertIsInstance(event_store, EventStore)
