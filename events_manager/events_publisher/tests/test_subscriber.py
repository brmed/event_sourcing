import mock
from django.test import TestCase
from .. import Subscriber


class SubscriberTestCase(TestCase):

    def setUp(self):
        self.event1, self.event2 = mock.Mock(), mock.Mock()
        self.handler1, self.handler2 = mock.Mock(), mock.Mock()
        self.subscriptions = [
            (self.event1, self.handler1),
            (self.event2, self.handler2),
        ]
        self.subscriber = Subscriber()

    def test_instantiate(self):
        self.assertIsInstance(self.subscriber, Subscriber)

    def test_subscribe(self):
        self.subscriber.subscribe(self.subscriptions)
        self.event1.connect_signal.assert_called_once_with(self.handler1)
        self.event2.connect_signal.assert_called_once_with(self.handler2)
