from typing import Optional, Any, List, Generator
from secops_toolkit.clients.secops_feature_clients.base import SecOpsBaseClient

from secops_toolkit.model.secops.rules_model import RuleList, Rule, RuleDeployment, VerifyRuleResponse


class RulesClient(SecOpsBaseClient):
    """Client for managing YARA-L rules in Google SecOps."""

    def list_rules(self, page_size: int = 100, page_token: Optional[str] = None) -> RuleList:
        """
        Retrieves a list of detection rules from the Google SecOps Instance.
        Ref: https://docs.cloud.google.com/chronicle/docs/reference/rest/v1beta/projects.locations.instances.rules
        """
        list_rules_url = self._craft_url("rules")
        params: dict[str, Any] = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token

        response = self._request("GET", list_rules_url, params=params)
        if not response:
            return RuleList(rules=[], next_page_token="")
        return RuleList(**response)

    def get_rule(self, rule_id: str) -> Optional[Rule]:
        """
        Retrieves a single detection rule.
        Ref: https://docs.cloud.google.com/chronicle/docs/reference/rest/v1beta/projects.locations.instances.rules/get
        """
        get_rule_url = self._craft_url("rules", rule_id)
        response = self._request("GET", get_rule_url)
        if not response:
            return None
        return Rule(**response)

    def get_rule_deployment(self, rule_id: str) -> Optional[RuleDeployment]:
        """
        Retrieves the deployment status of a specific rule.
        """
        deployment_url = self._craft_url("rules", rule_id, "deployment")
        response = self._request("GET", deployment_url)
        if not response:
            return None
        return RuleDeployment(**response)

    def list_all_rules(self, page_size: int = 100, name_filter: Optional[str] = None, limit: Optional[int] = None) -> Generator[Rule, None, None]:
        """A generator that automatically handles pagination to yield all rules."""
        next_token = None
        count = 0
        while True:
            response = self.list_rules(page_size=page_size, page_token=next_token)

            for rule in response.rules:
                if name_filter and name_filter.lower() not in (rule.display_name or rule.name).lower():
                    continue

                yield rule
                count += 1
                if limit and count >= limit:
                    return

            # Check if there are more pages
            next_token = response.next_page_token
            if not next_token:
                break

    def verify_rule_text(self, rule_text: str) -> Optional[VerifyRuleResponse]:
        """Verifies the syntax of a rule locally without saving it."""
        url = f"{self._get_api_parent(override_version='v1alpha')}:verifyRuleText"
        payload = {"ruleText": rule_text}     
        response = self._request("POST", url, json=payload)
        
        if not response:
            return None
        return VerifyRuleResponse(**response)

    def run_test_rule(self, rule_text: str, start_time: str, end_time: str) -> Optional[dict]:
        """Runs a legacy retro-hunt test rule on the instance."""
        url = f"{self._get_api_parent(override_version='v1alpha')}/legacy:legacyRunTestRule"
        payload = {
            "ruleText": rule_text,
            "timeRange": {
                "startTime": start_time,
                "endTime": end_time
            }
        }
        return self._request("POST", url, json=payload)

    def create_rule(self, rule_text: str) -> Optional[Rule]:
        """Creates a new rule."""
        url = self._craft_url("rules")
        payload = {"text": rule_text}
        response = self._request("POST", url, json=payload)
        return Rule(**response) if response else None

    def update_rule(self, rule_id: str, rule_text: str) -> Optional[Rule]:
        """Updates an existing rule."""
        url = self._craft_url("rules", rule_id)
        payload = {"text": rule_text}
        params = {"updateMask": "text"}
        response = self._request("PATCH", url, json=payload, params=params)
        return Rule(**response) if response else None
