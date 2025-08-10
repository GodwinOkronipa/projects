def simple_gcp_api(service_name, version, api_method, **kwargs):

# --- Google Cloud API Utility ---
# This script demonstrates advanced usage of Google Cloud authentication and API invocation.
# It is designed to be modular, reusable, and production-ready for cloud functions or automation scripts.

import google.auth
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

def simple_gcp_api(service_name, version, api_method, **kwargs):
    """
    Authenticates with Google Cloud, builds a service client, and executes a specified API method.
    This function is flexible and can be used for any Google Cloud API that supports discovery.

    Args:
        service_name (str): The name of the GCP service (e.g., 'drive', 'compute', 'cloudfunctions').
        version (str): The version of the API (e.g., 'v1').
        api_method (str): The method path to call (e.g., 'projects.list').
        **kwargs: Arguments to pass to the API method.

    Returns:
        dict: The response from the API call.
    """
    # Obtain default credentials with the required scope for the service
    creds, _ = google.auth.default (scopes=[f'https://www.googleapis.com/auth/{service_name}'])
    
    # Refresh credentials if expired
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        
    # Build the service client
    service = build(service_name, version, credentials=creds)
    
    # Traverse the API method path (e.g., 'projects.list')
    method = service
    for attr in api_method.split('.'):
        method = getattr(method, attr)
    try:
        # Execute the API call with provided arguments
        response = method(**kwargs).execute()
        logging.info(f"Successfully called {service_name}.{api_method}")
        return response
    except HttpError as e:
        logging.error(f"API call failed: {e}")
        return {"error": str(e)}


# --- Example: List Google Cloud Functions in a Project ---
if __name__ == "__main__":
    # Set up logging for better observability
    logging.basicConfig(level=logging.INFO)
    # Example usage: List all Cloud Functions in a project and region
    project_id = "your-gcp-project-id"  # TODO: Replace with your project ID
    region = "us-central1"  # TODO: Replace with your region
    try:
        functions = simple_gcp_api(
            service_name="cloudfunctions",
            version="v1",
            api_method="projects.locations.functions.list",
            parent=f"projects/{project_id}/locations/{region}"
        )
        print("Cloud Functions:", functions)
    except Exception as ex:
        logging.error(f"Failed to list Cloud Functions: {ex}")