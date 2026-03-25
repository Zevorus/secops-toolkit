import re
from typing import Optional
from secops_toolkit.model.secops.rules_model import RuleName

RULE_NAME_REGEX = re.compile(
    r"^projects\/(?P<project_number>\d+)\/locations\/(?P<location>[a-zA-Z0-9-]+)\/instances\/(?P<instance_uuid>[a-zA-Z0-9-]+)\/rules\/(?P<rule_id>ru_[a-zA-Z0-9-]+)$"
)

def parse_rule_name(name: str) -> Optional[RuleName]:
    """
    Parses a Google SecOps Rule deployment resource name into a Pydantic object.
    Returns None if the format is invalid.
    """
    match = RULE_NAME_REGEX.match(name)
    if not match:
        return None
    
    return RuleName(**match.groupdict())
