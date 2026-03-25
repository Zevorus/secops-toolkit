from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import Optional, Any, List, Dict
from secops_toolkit.model.common import PaginatedResponse
from datetime import datetime


class RuleType(str, Enum):
    RULE_TYPE_UNSPECIFIED = "RULE_TYPE_UNSPECIFIED"
    SINGLE_EVENT = "SINGLE_EVENT"
    MULTI_EVENT = "MULTI_EVENT"


class RunFrequency(str, Enum):
    RUN_FREQUENCY_UNSPECIFIED = "RUN_FREQUENCY_UNSPECIFIED"
    LIVE = "LIVE"
    HOURLY = "HOURLY"
    DAILY = "DAILY"


class CompilationState(str, Enum):
    COMPILATION_STATE_UNSPECIFIED = "COMPILATION_STATE_UNSPECIFIED"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class Severity(str, Enum):
    SEVERITY_UNSPECIFIED = "SEVERITY_UNSPECIFIED"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ExecutionState(str, Enum):
    EXECUTION_STATE_UNSPECIFIED = "EXECUTION_STATE_UNSPECIFIED"
    DEFAULT = "DEFAULT"
    LIMITED = "LIMITED"
    PAUSED = "PAUSED"


class CompilationDiagnostic(BaseModel):
    message: str = Field()
    severity: Optional[Severity] = Field(None)
    # position is often an object with line/column
    # ref: https://docs.cloud.google.com/chronicle/docs/reference/rest/v1beta/projects.locations.instances.rules#Rule.CompilationDiagnostic


class InputsUsed(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    data_table_resource_names: List[str] = Field([], alias="dataTableResourceNames")
    uses_udm: bool = Field(False, alias="usesUdm")


class Rule(BaseModel):
    """
    Represents the definition and metadata of a detection rule.
    Ref: https://docs.cloud.google.com/chronicle/docs/reference/rest/v1beta/projects.locations.instances.rules
    """
    model_config = ConfigDict(populate_by_name=True)
    name: str = Field()
    revision_id: Optional[str] = Field(None, alias="revisionId")
    display_name: Optional[str] = Field(None, alias="displayName")
    text: Optional[str] = Field(None)
    author: Optional[str] = Field(None)
    severity: Optional[Severity] = Field(None)
    metadata: Optional[Dict[str, str]] = Field(None)
    create_time: Optional[datetime] = Field(None, alias="createTime")
    revision_create_time: Optional[datetime] = Field(None, alias="revisionCreateTime")
    compilation_state: Optional[CompilationState] = Field(None, alias="compilationState")
    rule_type: Optional[RuleType] = Field(None, alias="type")
    reference_lists: List[str] = Field([], alias="referenceLists")
    allowed_run_frequencies: List[RunFrequency] = Field([], alias="allowedRunFrequencies")
    etag: Optional[str] = Field(None)
    scope: Optional[str] = Field(None)
    compilation_diagnostics: List[CompilationDiagnostic] = Field([], alias="compilationDiagnostics")
    near_real_time_live_rule_eligible: bool = Field(False, alias="nearRealTimeLiveRuleEligible")
    inputs_used: Optional[InputsUsed] = Field(None, alias="inputsUsed")


class RuleDeployment(BaseModel):
    """
    Represents the deployment settings and status for a rule.
    Ref: https://docs.cloud.google.com/chronicle/docs/reference/rest/v1beta/projects.locations.instances.rules/deployment
    """
    model_config = ConfigDict(populate_by_name=True)
    name: str = Field()
    enabled: bool = Field(True)
    alerting: bool = Field(True)
    archived: bool = Field(False)
    archive_time: Optional[datetime] = Field(None, alias="archiveTime")
    run_frequency: Optional[RunFrequency] = Field(None, alias="runFrequency")
    execution_state: Optional[ExecutionState] = Field(None, alias="executionState")
    last_alert_status_change_time: Optional[datetime] = Field(None, alias="lastAlertStatusChangeTime")


class RuleList(PaginatedResponse):
    """Lists Rules."""
    model_config = ConfigDict(populate_by_name=True)
    rules: List[Rule] = Field([], alias="rules")


class RuleName(BaseModel):
    """Breaks down the full resource name into its component parts."""
    project_number: str
    location: str
    instance_uuid: str
    rule_id: str



