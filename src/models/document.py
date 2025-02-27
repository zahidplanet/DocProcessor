"""
Document models for the DocProcessor application.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    """Types of documents that can be processed."""
    
    SAFETY_RISK_ASSESSMENT = "Safety Risk Assessment"
    FUNCTIONAL_PROGRAM = "Functional Program"
    EQUIPMENT_LIST = "Equipment List"
    OTHER = "Other"


class DocumentStatus(str, Enum):
    """Status of a document in the review process."""
    
    UPLOADED = "Uploaded"
    IN_REVIEW = "In Review"
    REVIEWED = "Reviewed"
    UPDATED = "Updated"
    APPROVED = "Approved"
    RESUBMITTED = "Resubmitted"


class CommentStatus(str, Enum):
    """Status of a review comment."""
    
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    APPROVED = "Approved"


class Comment(BaseModel):
    """A review comment on a document."""
    
    id: Optional[str] = None
    document_id: str
    text: str
    page_number: Optional[int] = None
    section: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    status: CommentStatus = CommentStatus.OPEN
    resolution_text: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    related_comment_ids: List[str] = Field(default_factory=list)


class Document(BaseModel):
    """A document in the system."""
    
    id: Optional[str] = None
    filename: str
    original_filename: str
    document_type: DocumentType
    upload_date: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)
    status: DocumentStatus = DocumentStatus.UPLOADED
    version: int = 1
    comments: List[Comment] = Field(default_factory=list)
    parent_document_id: Optional[str] = None  # For tracking document versions
    metadata: dict = Field(default_factory=dict)  # For extensibility 