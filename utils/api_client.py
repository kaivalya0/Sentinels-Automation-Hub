# utils/api_client.py
from playwright.sync_api import APIRequestContext

class APIClient:
    def __init__(self, request: APIRequestContext):
        """
        Uses Playwright's native Request Context for session sharing.
        This allows API calls to reuse the UI's login state.
        """
        self.request = request

    def post(self, endpoint: str, data: dict = None, headers: dict = None):
        """Standardized POST method for setup actions."""
        response = self.request.post(endpoint, data=data, headers=headers)
        return self._handle_response(response)

    def get(self, endpoint: str, params: dict = None, headers: dict = None):
        """Standardized GET method for data validation."""
        response = self.request.get(endpoint, params=params, headers=headers)
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response):
        """
        Internal utility to validate status and return JSON.
        Prevents 'Silent Failures'—if the API crashes, the test stops.
        """
        if not response.ok:

            raise Exception(f"API Error: {response.status} - {response.text()}")

        return response.json()