from typing import Optional, Any, List, Mapping, Generator
from secops_toolkit.clients.secops_feature_clients.base import SecOpsBaseClient

from secops_toolkit.model.secops.rules_model import RuleList
from secops_toolkit.model.secops.rules_model import Rule

class RulesClient(SecOpsBaseClient):
    """Client for managing YARA-L rules in Google SecOps."""
    
    def list_rules(self, page_size: Optional[int] = 100, page_token: Optional[str] = None) -> RuleList:
        """
            Retrieves a list of detection rules from the Google SecOps Instance.
            ref: https://docs.cloud.google.com/chronicle/docs/reference/rest/v1beta/projects.locations.instances.rules
        """ 
        list_rules_url = self._craft_url("rules")
        params = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token
            
        response = self._request("GET", list_rules_url, params=params)
        return RuleList(**response)

    def list_all_rules(self, page_size: int = 100) -> Generator[Rule, None, None]:
        """A generator that automatically handles pagination to yield all rules."""
        next_token = None
        while True:
            response = self.list_rules(page_size=page_size, page_token=next_token)
            
            for rule in response.rules:
                yield rule
            
            # Check if there are more pages
            next_token = response.next_page_token
            if not next_token:
                break
