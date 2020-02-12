from django.test import TestCase
import mock

from datetime import date
from decimal import Decimal

from ..json_utils import SerializableDict, json


class JsonUtilsTestCase(TestCase):
    def setUp(self):
        self.serializable_dict = SerializableDict

        self.address = mock.Mock(
            street='Avenida Padre Leonel Franca',
            number=90,
        )

        self.father = mock.Mock(
            first_name='Arthur',
            address=self.address,
            date_of_birth=date(1964, 2, 15),
        )

        self.mother = mock.Mock(
            first_name='Maria',
            address=self.address,
            date_of_birth=date(1966, 4, 8),
        )

        self.student = dict(
            first_name='Rodrigo',
            parents=[self.father, self.mother],
            address=self.address,
            date_of_birth=date(1993, 11, 17),
            grade=Decimal(8),
        )

        self.father.to_dict.return_value = dict(
            first_name='Arthur',
            address=self.address,
            date_of_birth=date(1964, 2, 15),
        )

        self.mother.to_dict.return_value = dict(
            first_name='Maria',
            address=self.address,
            date_of_birth=date(1966, 4, 8),
        )

        self.address.to_dict.return_value = dict(
            street='Avenida Padre Leonel Franca',
            number=90,
        )

        self.serialized_student = {
            'first_name': 'Rodrigo',
            'parents': [
                {
                    'first_name': 'Arthur',
                    'address': {
                        'street': 'Avenida Padre Leonel Franca',
                        'number': 90,
                    },
                    'date_of_birth': '1964-02-15',
                },
                {
                    'first_name': 'Maria',
                    'address': {
                        'street': 'Avenida Padre Leonel Franca',
                        'number': 90,
                    },
                    'date_of_birth': '1966-04-08',
                },
            ],
            'address': {
                'street': 'Avenida Padre Leonel Franca',
                'number': 90,
            },
            'date_of_birth': '1993-11-17',
            'grade': '8',
        }

    def test_serializing_dict_with_to_dict_method(self):
        self.assertEqual(
            self.serialized_student,
            self.serializable_dict(self.student),
        )

        self.father.to_dict.assert_called()
        self.mother.to_dict.assert_called()
        self.address.to_dict.assert_called()

    def test_serializing_dict_without_to_dict_method(self):
        del self.father.to_dict, self.mother.to_dict, self.address.to_dict
        del self.father.method_calls, self.mother.method_calls, self.address.method_calls

        self.assertEqual(
            self.serialized_student,
            self.serializable_dict(self.student),
        )

    def test_custom_encoder_dumping_and_loading_serializable_dict(self):
        self.assertEqual(
            self.serialized_student,
            json.loads(json.dumps(self.student)),
        )
