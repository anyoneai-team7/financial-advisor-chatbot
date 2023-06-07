import unittest
from unittest.mock import patch
from app import app


class AskModelTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the Flask app and client for testing
        self.app = app.test_client()

    def test_ask_model_with_valid_data(self):
        # Define a sample request JSON
        request_data = {
            "messages": ["message1", "message2", "message3"],
            "user": "user1",
        }

        # Mock the model_predict function
        with patch("views.model_predict") as mock_model_predict:
            mock_model_predict.return_value = "Mocked response"

            # Send a POST request to the endpoint
            response = self.app.post("/api/ask_model", json=request_data)

            # Assert the response
            self.assertEqual(response.status_code, 200)
            expected_response = {"user": "user1", "content": "Mocked response"}
            self.assertEqual(response.get_json(), expected_response)

    def test_ask_model_with_invalid_data(self):
        # Send a POST request without the required JSON fields
        response = self.app.post("/api/ask_model", json={})

        # Assert the response
        self.assertEqual(response.status_code, 500)
