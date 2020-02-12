import mock
from django.test import TestCase
from .. import Publisher


class PublisherTestCase(TestCase):

    def setUp(self):
        self.events = [mock.Mock(), mock.Mock(), mock.Mock()]
        self.publisher = Publisher()
        self.subscription = dict(event_class=mock.Mock(), handler=mock.Mock())

    def test_initialize(self):
        self.assertIsInstance(self.publisher, Publisher)

    def test_publish(self):
        self.publisher.publish(*self.events)
        for e in self.events:
            e.notify.assert_called_once_with()
