from django.test import TestCase
from rest_framework.test import APIClient


class RouteAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/route/"

    def test_invalid_payload(self):
        """API should reject invalid coordinate format"""
        response = self.client.post(self.url, {"start": "NYC"}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_valid_request_structure(self):
        """API should return expected keys for valid request"""
        response = self.client.post(
            self.url,
            {
                "start": [-118.2437, 34.0522],
                "end": [-117.1611, 32.7157],
            },
            format="json"
        )

        self.assertIn(response.status_code, (200, 502))  # allow routing API unavailable

        if response.status_code == 200:
            self.assertIn("summary", response.data)
            self.assertIn("fuel_stops", response.data)
