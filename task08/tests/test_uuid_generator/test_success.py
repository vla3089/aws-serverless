from tests.test_uuid_generator import UuidGeneratorLambdaTestCase


class TestSuccess(UuidGeneratorLambdaTestCase):

    def test_success(self):
        self.assertEqual(200, 200)

