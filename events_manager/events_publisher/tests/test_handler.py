import mock
from django.test import TestCase
from .. import Handler


class HandlerTestCase(TestCase):

    def setUp(self):
        self.handler = Handler()

    def test_instantiate(self):
        self.assertIsInstance(self.handler, Handler)

    @mock.patch.object(Handler, 'run')
    def test_is_callable(self, run):
        args = 1, 2
        kwargs = dict(span='eggs')
        self.handler(*args, **kwargs)
        run.assert_called_once_with(*args, **kwargs)

    def test_uid_returns_class(self):
        self.assertEqual(self.handler.uid, self.handler.__class__)
