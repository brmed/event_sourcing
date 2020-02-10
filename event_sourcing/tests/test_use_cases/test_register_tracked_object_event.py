from django.test import TestCase

from event_sourcing.use_cases import RegisterTrackedObjectEvent

from event_sourcing.domain import TrackedObject

import mock


class RegisterTrackedObjectEventTestCase(TestCase):
    def setUp(self):
        self.tracked_object = TrackedObject()
        self.user = mock.Mock()
        self.event = mock.Mock()
        self.event_date = mock.Mock()
        self.event_name = mock.Mock()

        self.repository = mock.Mock()
        self.factory = mock.Mock()

        self.use_case = RegisterTrackedObjectEvent(
            repository=self.repository,
            factory=self.factory,
        )

        self.factory.build_event_from_tracked_object.return_value = self.event
        self.repository.get_last_event.return_value = self.event

    def test_instantiate(self):
        self.assertIsInstance(self.use_case, RegisterTrackedObjectEvent)

    def test_should_ask_for_event_store_factory_to_build_event(self):
        self.use_case.execute(
            self.tracked_object,
            self.user,
            event_name=self.event_name,
            event_date=self.event_date,
        )
        self.factory.build_event_from_tracked_object.assert_called_once_with(
            tracked_object=self.tracked_object,
            user=self.user,
            name=self.event_name,
            date=self.event_date,
        )

    def test_should_ask_event_store_repository_for_last_event(self):
        self.use_case.execute(
            self.tracked_object,
            self.user,
        )

        self.repository.get_last_event.assert_called_once_with(
            self.tracked_object,
        )

    def test_should_ask_for_event_store_repository_to_save_event(self):
        self.use_case.execute(
            self.tracked_object,
            self.user,
        )

        self.repository.save_event.assert_called_once_with(
            self.event,
            self.tracked_object,
        )
