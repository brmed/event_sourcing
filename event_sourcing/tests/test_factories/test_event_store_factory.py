from django.test import TestCase
from model_mommy import mommy
import mock
import datetime

from event_sourcing.models import (
    EventStore as EventStoreModel,
    Event as EventModel
)

from event_sourcing.domain import (
    EventStore as EventStoreDomain,
    Event as EventDomain,
    TrackedObject,
)

from event_sourcing.factories import EventStoreFactory

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class EventStoreFactoryTestCase(TestCase):
    def setUp(self):
        self.user = mommy.make(UserModel)

        self.user_domain = mock.Mock(
            id=20,
            username='sudo',
            first_name='Rodrigo',
            email='rodrigo@moobile.com.br'
        )

        self.event_store_model = mommy.make(
            EventStoreModel,
        )

        self.event_model = mommy.make(
            EventModel,
            name='Evento de Criação',
            user=self.user,
            event_store=self.event_store_model,
            diff=None,
            state={
                'nome': 'Rodrigo Bello',
                'email': 'rodrigo@moobile.com.br',
                'idade': '25',
            }
        )

        self.factory = EventStoreFactory()

        self.event_store_domain = self.factory.build_from_model(
            self.event_store_model
        )

    def test_instantiate(self):
        self.assertIsInstance(self.factory, EventStoreFactory)

    def test_build_event_from_model(self):
        event_domain = self.factory.build_event_from_model(self.event_model)

        self.assertEqual(
            event_domain.name,
            self.event_model.name,
        )

        self.assertEqual(
            event_domain.date,
            self.event_model.date,
        )

        self.assertEqual(
            event_domain.user.id,
            self.user.id,
        )

        self.assertEqual(
            event_domain.diff,
            self.event_model.diff,
        )

        self.assertEqual(
            event_domain.state,
            self.event_model.state,
        )

    def test_build_event_store_from_model(self):
        event_domain = self.event_store_domain.get_last_event()
        tracked_object = self.event_store_domain.tracked_object

        self.assertIsInstance(self.event_store_domain, EventStoreDomain)
        self.assertIsInstance(event_domain, EventDomain)
        self.assertIsInstance(tracked_object, TrackedObject)

    def test_build_event_from_tracked_object(self):
        tracked_object = TrackedObject(
            object_id=20,
            module='apps.event_sourcing.domain',
            signature='TrackedObject',
        )

        date = datetime.datetime.now()

        event_domain = self.factory.build_event_from_tracked_object(
            user=self.user_domain,
            tracked_object=tracked_object,
            name='Evento de Criação',
            date=date
        )

        self.assertEqual(
            event_domain.name, 'Evento de Criação'
        )

        self.assertEqual(
            event_domain.state,
            dict(
                object_id=20,
                module='apps.event_sourcing.domain',
                signature='TrackedObject',
            )
        )

        self.assertEqual(
            event_domain.date,
            date
        )

        self.assertEqual(
            event_domain.user.id,
            self.user_domain.id,
        )
