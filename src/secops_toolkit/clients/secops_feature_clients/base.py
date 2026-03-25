import os
import logging
from typing import Optional, Any
from google.auth.transport.requests import AuthorizedSession
from google.auth import default
from requests import HTTPError
from dotenv import load_dotenv, find_dotenv

LOGGER = logging.getLogger(__name__)


class SecOpsBaseClient:
    """Base client sharing common functionality for Google SecOps."""

    def __init__(self, version: str = "v1beta"):
        # Ensure environment is loaded
        load_dotenv(find_dotenv())

        self.base_url = os.getenv("SECOPS_API_ENDPOINT")
        self.project_number = os.getenv("SECOPS_PROJECT_NUMBER")
        self.instance_id = os.getenv("SECOPS_INSTANCE_ID")
        self.location = os.getenv("SECOPS_LOCATION")
        self.version = version

        # Authentication parameters
        self.credentials, _project_id = default()
        self.session = AuthorizedSession(self.credentials)

    def set_version(self, version: str) -> None:
        self.version = version

    def _get_api_endpoint(self) -> str:
        return f"{self.base_url}/{self.version}"
    
    def _get_api_parent(self) -> str:
        # Google SecOps Resource Name Format: "projects/{PROJECT}/locations/{LOCATION}/instances/{INSTANCE}"
        return f"{self._get_api_endpoint()}/projects/{self.project_number}/locations/{self.location}/instances/{self.instance_id}"

    def _craft_url(self, *path_entries) -> str:
        return f"{self._get_api_parent()}/{'/'.join(path_entries)}"

    def _request(self, method: str, url: str, **kwargs) -> Optional[dict[str, Any]]:
        """Handles HTTP requests with error logging."""
        response = self.session.request(method, url, **kwargs)
        try:
            response.raise_for_status()
            if response.status_code == 204:
                return {}
            return response.json()
        except HTTPError as e:
            LOGGER.error(f"HTTP Error {response.status_code}: {e.response.text}")
            return None
        except Exception as e:
            LOGGER.error(f"Error during request: {e}")
            return None
