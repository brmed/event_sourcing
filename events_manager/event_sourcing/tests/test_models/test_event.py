from django.test import TestCase
from model_mommy import mommy
from event_sourcing.models import Event


class EventModelTestCase(TestCase):
    def test_instantiate(self):
        event = mommy.make(Event)
        self.assertIsInstance(event, Event)
