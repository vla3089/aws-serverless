from tests.test_hello_lambda import HelloLambdaLambdaTestCase


class TestSuccess(HelloLambdaLambdaTestCase):

    def test_success(self):
        content = {
                "statusCode": 200,
                "message": "Hello from Lambda"
            }
        self.assertEqual(self.HANDLER.handle_request(dict(), dict()), content)

