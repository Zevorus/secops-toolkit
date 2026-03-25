from typing import Optional, Any
from secops_toolkit.clients.secops_feature_clients.rules import RulesClient
from secops_toolkit.clients.secops_feature_clients.base import SecOpsBaseClient

class SecOpsClient(SecOpsBaseClient):
    """
    Main Google SecOps Client.
    Modularized to delegate specific functionality to mini-clients.
    """
    
    def __init__(self, version: str = "v1beta"):
        super().__init__(version=version)
        
        # seopcs-feature-clients
        self.rules = RulesClient(version=version)

    def test_connectivity(self) -> bool:
        """Test REST API connectivity by running a trivial API call."""
        # Use an instance metadata call to test connectivity
        instance_url = self._get_api_parent()
        return self._request("GET", instance_url) is not None
