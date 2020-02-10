from django.test import TestCase

from event_sourcing.domain import (
    TrackedObject
)

import mock


class TrackedObjectTestCase(TestCase):
    def setUp(self):
        class Student(TrackedObject):
            def __init__(self, name, address, age, UNTRACKED_FIELDS=None):
                self.name = name
                self.address = address
                self.age = age
                if UNTRACKED_FIELDS:
                    self.UNTRACKED_FIELDS = UNTRACKED_FIELDS

        self.tracked_object = Student

        self.address = mock.Mock(
            street='Avenida Padre Leonel Franca',
            number=90,
        )

        self.address.to_dict.return_value = dict(
            street='Avenida Padre Leonel Franca',
            number=90,
        )

        self.attributes = dict(
            name='Rodrigo',
            address=self.address,
            age=25,
        )

    def test_instantiate(self):
        tracked_object = self.tracked_object(**self.attributes)
        self.assertIsInstance(tracked_object, TrackedObject)

    def test_get_state_without_ignored_fields(self):
        tracked_object = self.tracked_object(**self.attributes)

        self.assertEqual(
            tracked_object.get_state(),
            {
                'name': 'Rodrigo',
                'address': {
                    'street': 'Avenida Padre Leonel Franca',
                    'number': 90,
                },
                'age': 25,
            }
        )

    def test_get_state_with_one_simple_untracked_field(self):
        tracked_object = self.tracked_object(
            **self.attributes,
            UNTRACKED_FIELDS=('name',)
        )

        self.assertEqual(
            tracked_object.get_state(),
            {
                'address': {
                    'street': 'Avenida Padre Leonel Franca',
                    'number': 90,
                },
                'age': 25,
                'UNTRACKED_FIELDS': ('name',)
            }
        )

    def test_get_state_with_two_simple_untracked_fields(self):
        tracked_object = self.tracked_object(
            **self.attributes,
            UNTRACKED_FIELDS=('name', 'age')
        )

        self.assertEqual(
            tracked_object.get_state(),
            {
                'address': {
                    'street': 'Avenida Padre Leonel Franca',
                    'number': 90,
                },
                'UNTRACKED_FIELDS': ('name', 'age')
            }
        )

    def test_get_state_with_one_depth_untracked_field(self):
        tracked_object = self.tracked_object(
            **self.attributes,
            UNTRACKED_FIELDS=('address__street',)
        )

        self.assertEqual(
            tracked_object.get_state(),
            {
                'name': 'Rodrigo',
                'address': {
                    'number': 90,
                },
                'age': 25,
                'UNTRACKED_FIELDS': ('address__street',)
            }
        )

    def test_get_state_with_two_depth_untracked_fields(self):
        tracked_object = self.tracked_object(
            **self.attributes,
            UNTRACKED_FIELDS=('address__street', 'address__number')
        )

        self.assertEqual(
            tracked_object.get_state(),
            {
                'name': 'Rodrigo',
                'address': {},
                'age': 25,
                'UNTRACKED_FIELDS': ('address__street', 'address__number'),
            }
        )
