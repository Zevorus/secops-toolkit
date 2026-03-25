import os
import json
import logging
from typing import List, Optional
import google.auth
from google.auth.transport import requests
from google.oauth2 import service_account

LOGGER = logging.getLogger(__name__)

AUTHORIZATION_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

def initialize_http_session(scopes: Optional[List[str]] = None) -> requests.AuthorizedSession:
  """Initializes an authorized HTTP session for Google Cloud APIs."""

  auth_method = os.environ.get("GOOGLE_AUTHENTICATION_TYPE", "APPLICATION_DEFAULT_CREDENTIALS")
  credentials = None
  
  effective_scopes = scopes or AUTHORIZATION_SCOPES

  if auth_method == "APPLICATION_DEFAULT_CREDENTIALS":
    LOGGER.debug("Authenticating using Application Default Credentials")
    credentials, _ = google.auth.default(scopes=effective_scopes)

  elif auth_method == "SERVICE_ACCOUNT_KEY":
    LOGGER.debug("Authenticating using service account key")
    service_account_key = os.environ.get("GOOGLE_SECOPS_SERVICE_ACCOUNT_KEY")
    if not service_account_key:
        raise EnvironmentError("GOOGLE_SECOPS_SERVICE_ACCOUNT_KEY environment variable not set")
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(service_account_key),
        scopes=effective_scopes,
    )

  return requests.AuthorizedSession(credentials)
