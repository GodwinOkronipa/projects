import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

class GCloudAPI:
    def __init__(self, service_name, version, credentials_json):
        self.service_name = service_name
        self.version = version
        self.credentials_json = credentials_json
        self.service = None
        self._authenticate()

    def _authenticate(self):
        try:
            credentials = service_account.Credentials.from_service_account_file(self.credentials_json)
            self.service = build(self.service_name, self.version, credentials=credentials)
            logging.info(f"Authenticated to {self.service_name} API v{self.version}")
        except Exception as e:
            logging.error(f"Authentication failed: {e}")
            self.service = None

    def call(self, resource, method, **kwargs):
        if not self.service:
            logging.error("Service not authenticated.")
            return None
        try:
            api_resource = getattr(self.service, resource)()
            api_method = getattr(api_resource, method)
            response = api_method(**kwargs).execute()
            logging.info(f"API call to {resource}.{method} succeeded.")
            return response
        except HttpError as e:
            logging.error(f"Google API error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        return None

# Example usage (uncomment and fill in your details):
# api = GCloudAPI('drive', 'v3', 'path/to/credentials.json')
# result = api.call('files', 'list', pageSize=10)
# print(result)
