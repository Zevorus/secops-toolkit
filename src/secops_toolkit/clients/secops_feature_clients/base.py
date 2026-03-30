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

    def __init__(
        self,
        version: str = "v1beta",
        credentials: Optional[Any] = None,
        session: Optional[AuthorizedSession] = None,
    ):
        # Ensure environment is loaded
        # 1. Load Global active profile first
        from secops_toolkit.utils.config_manager import get_global_config_path
        global_path = get_global_config_path()
        if global_path:
            load_dotenv(global_path)

        # 2. Support local .env override (True means it overwrites Global)
        load_dotenv(find_dotenv(), override=True)

        self.base_url = os.getenv("SECOPS_API_ENDPOINT")
        self.project_number = os.getenv("SECOPS_PROJECT_NUMBER")
        self.instance_id = os.getenv("SECOPS_INSTANCE_ID")
        self.location = os.getenv("SECOPS_REGION")

        self._validate_env()

        self.version = version

        # Authentication parameters
        if credentials and session:
            self.credentials = credentials
            self.session = session
        else:
            self.credentials, _project_id = default()
            self.session = AuthorizedSession(self.credentials)

    def set_version(self, version: str) -> None:
        self.version = version

    def _get_api_endpoint(self, override_version: Optional[str] = None) -> str:
        version = override_version or self.version
        return f"{self.base_url}/{version}"
    
    def _get_api_parent(self, override_version: Optional[str] = None) -> str:
        # Google SecOps Resource Name Format: "projects/{PROJECT}/locations/{LOCATION}/instances/{INSTANCE}"
        return f"{self._get_api_endpoint(override_version)}/projects/{self.project_number}/locations/{self.location}/instances/{self.instance_id}"

    def _craft_url(self, *path_entries, override_version: Optional[str] = None) -> str:
        return f"{self._get_api_parent(override_version)}/{'/'.join(path_entries)}"

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

    def _validate_env(self):
        for attribute, value in self.__dict__.items():
            if value is None:
                raise RuntimeError(f"Missing required environment variable: {attribute}")
