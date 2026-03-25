import os
import logging
import json
from typing import Optional, Any
from dotenv import load_dotenv, find_dotenv
from google.auth.transport.requests import AuthorizedSession
from requests import HTTPError
from google.auth import default

load_dotenv(dotenv_path=find_dotenv())

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

class SecOpsClient:
    def __init__(self, version="v1beta"):
        # secops instance parameters
        self.base_url = os.getenv("API_ENDPOINT")
        self.project_number = os.getenv("SECOPS_PROJECT_NUMBER")
        self.instance_id = os.getenv("SECOPS_INSTANCE_ID")
        self.location = os.getenv("SECOPS_LOCATION")
        self.version = version

        # authentication parameters
        self.credentials, _project_id = default()
        self.session = AuthorizedSession(self.credentials)

    def test_connectivity(self) -> bool:
        """
            Test REST API connectivity by running a trivial API call
        """

        return True if (self._get_instance_details()) else False

    def list_rules(self, page_size: Optional[int] = 100, page_token: Optional[str] = None) -> Optional[list[dict[str, Any]]]:
        """
            Retrieves a list of detection rules from the Google SecOps Instance.
        """

        list_rules_url = self._craft_rest_api_path("rules", "-","deployments")
        params = {"pageSize": page_size, "pageToken": page_token}
        response = self.session.get(list_rules_url, params=params)
        
        try:
            response.raise_for_status()
            return response.json()
        except HTTPError as http_error:
            logging.error(f"Failed to list rules: {http_error}")
            return None

    def _get_instance_details(self) -> Optional[dict[str, Any]]:
        """
            Get basic information about the Google SecOps Instance
        """
        
        instance_url = self._get_rest_api_parent()
        
        logging.info(f"Requesting Instance Metadata: {instance_url}")
        response = self.session.get(instance_url)
        
        try:
            response.raise_for_status()
        except HTTPError as http_error:
            logging.error(f"Failed to request Instance Metadata: {http_error}")
            return None
        return response.json()

    def _get_rest_api_endpoint(self):
        return f"{self.base_url}/{self.version}"
    
    def _get_rest_api_parent(self):
        # Google SecOps Resource Name Format: "projects/{PROJECT}/locations/{LOCATION}/instances/{INSTANCE}"
        return f"{self._get_rest_api_endpoint()}/projects/{self.project_number}/locations/{self.location}/instances/{self.instance_id}"

    def _craft_rest_api_path(self, *path_entries):
        return f"{self._get_rest_api_parent()}/{"/".join(path_entries)}"

if __name__ == "__main__":
    client = SecOpsClient(version="v1beta")
    result = client.test_connectivity()

    rules = client.list_rules()
    print(rules)