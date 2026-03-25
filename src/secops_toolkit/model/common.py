from pydantic import BaseModel, Field
from typing import Optional, List

class PaginatedResponse(BaseModel):
    """
        Base class for anything that has a nextPageToken.
        Seen in:
            - projects.locations.instances.rules.deployments.list
    """
    next_page_token: Optional[str] = Field(None, alias="nextPageToken")
