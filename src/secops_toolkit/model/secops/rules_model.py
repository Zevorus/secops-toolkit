from pydantic import BaseModel, Field
from enum import Enum, IntEnum
from typing import Optional, Any, List, Literal
from secops_toolkit.model.common import PaginatedResponse
from datetime import datetime


class RuleTypeEnum(str, Enum):
    RULE_TYPE_UNSPECIFIED = "RULE_TYPE_UNSPECIFIED"
    SINGLE_EVENT = "SINGLE_EVENT"
    MULTI_EVENT = "MULTI_EVENT"

class RunFrequencyEnum(str, Enum):
    RUN_FREQUENCY_UNSPECIFIED = "RUN_FREQUENCY_UNSPECIFIED"
    LIVE = "LIVE"
    HOURLY = "HOURLY"
    DAILY = "DAILY"


class Rule(BaseModel):
    """
        The Rule resource represents a user-created rule.
        Ref: https://docs.cloud.google.com/chronicle/docs/reference/rest/v1beta/projects.locations.instances.rules
    """

    name: str = Field()
    revision_id: Optional[str] = Field(None, alias="revisionId")
    display_name: Optional[str] = Field(None, alias="displayName")
    text: Optional[str] = Field(None)
    author: Optional[str] = Field(None)
    severity: Optional[dict[str, str]] = Field(None)
    metadata: Optional[dict[str, str]] = Field(None)
    create_time: Optional[datetime] = Field(None, alias="createTime")
    revision_create_time: Optional[datetime] = Field(None, alias="revisionCreateTime")
    compilation_state: Optional[str] = Field(None, alias="compilationState")
    rule_type: Optional[RuleTypeEnum] = Field(None, alias="type")
    reference_lists: Optional[List[str]] = Field(None, alias="referenceLists")
    allowed_run_frequencies: Optional[List[RunFrequencyEnum]] = Field(None, alias="allowedRunFrequencies")
    etag: Optional[str] = Field(None)
    scope: Optional[str] = Field(None)
    compilation_diagnostics: Optional[List[dict[str, Any]]] = Field(None, alias="compilationDiagnostics")
    near_real_time_live_rule_eligible: Optional[bool] = Field(None, alias="nearRealTimeLiveRuleEligible")
    inputs_used: Optional[dict[str, Any]] = Field(None, alias="inputsUsed")

class RuleName(BaseModel):
    """Breaks down the full resource name into its component parts."""
    project_number: str
    location: str
    instance_uuid: str
    rule_id: str

class RuleList(PaginatedResponse):
    """
        Ref: https://docs.cloud.google.com/chronicle/docs/reference/rest/v1beta/projects.locations.instances.rules/list
        method: rules.list
        Lists Rules.
    """

    rules: List[Rule] = Field([], alias="rules")



