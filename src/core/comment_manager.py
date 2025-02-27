"""
Core functionality for managing comments on documents.
"""

import uuid
from datetime import datetime
from typing import List, Dict, Optional

from src.models.document import Document, Comment, CommentStatus


class CommentManager:
    """Manager for comments across documents."""
    
    def __init__(self):
        """Initialize the comment manager."""
        # In a real application, this would connect to a database
        self.comments: Dict[str, Comment] = {}
    
    def add_comment(self, document_id: str, text: str, page_number: Optional[int] = None,
                    section: Optional[str] = None) -> Comment:
        """
        Add a new comment to a document.
        
        Args:
            document_id: ID of the document to comment on
            text: Text of the comment
            page_number: Page number the comment refers to (optional)
            section: Section the comment refers to (optional)
            
        Returns:
            The newly created comment
        """
        comment_id = str(uuid.uuid4())
        comment = Comment(
            id=comment_id,
            document_id=document_id,
            text=text,
            page_number=page_number,
            section=section,
            created_at=datetime.now(),
            status=CommentStatus.OPEN
        )
        
        self.comments[comment_id] = comment
        return comment
    
    def update_comment_status(self, comment_id: str, status: CommentStatus) -> Comment:
        """
        Update the status of a comment.
        
        Args:
            comment_id: ID of the comment to update
            status: New status of the comment
            
        Returns:
            The updated comment
            
        Raises:
            KeyError: If the comment doesn't exist
        """
        if comment_id not in self.comments:
            raise KeyError(f"Comment {comment_id} not found")
            
        comment = self.comments[comment_id]
        comment.status = status
        comment.updated_at = datetime.now()
        
        return comment
    
    def resolve_comment(self, comment_id: str, resolution_text: str, 
                        resolved_by: str) -> Comment:
        """
        Mark a comment as resolved.
        
        Args:
            comment_id: ID of the comment to resolve
            resolution_text: Text explaining how the comment was resolved
            resolved_by: Name or ID of the user who resolved the comment
            
        Returns:
            The updated comment
            
        Raises:
            KeyError: If the comment doesn't exist
        """
        if comment_id not in self.comments:
            raise KeyError(f"Comment {comment_id} not found")
            
        comment = self.comments[comment_id]
        comment.status = CommentStatus.RESOLVED
        comment.resolution_text = resolution_text
        comment.resolved_by = resolved_by
        comment.resolved_at = datetime.now()
        comment.updated_at = datetime.now()
        
        return comment
    
    def get_comments_for_document(self, document_id: str) -> List[Comment]:
        """
        Get all comments for a document.
        
        Args:
            document_id: ID of the document to get comments for
            
        Returns:
            List of comments for the document
        """
        return [
            comment for comment in self.comments.values() 
            if comment.document_id == document_id
        ]
    
    def get_open_comments_for_document(self, document_id: str) -> List[Comment]:
        """
        Get all open comments for a document.
        
        Args:
            document_id: ID of the document to get comments for
            
        Returns:
            List of open comments for the document
        """
        return [
            comment for comment in self.comments.values() 
            if comment.document_id == document_id and comment.status == CommentStatus.OPEN
        ]
    
    def get_comment(self, comment_id: str) -> Comment:
        """
        Get a comment by ID.
        
        Args:
            comment_id: ID of the comment to get
            
        Returns:
            The comment
            
        Raises:
            KeyError: If the comment doesn't exist
        """
        if comment_id not in self.comments:
            raise KeyError(f"Comment {comment_id} not found")
            
        return self.comments[comment_id]
    
    def link_related_comments(self, comment_id: str, related_comment_ids: List[str]) -> Comment:
        """
        Link a comment to related comments.
        
        Args:
            comment_id: ID of the comment to link
            related_comment_ids: IDs of related comments
            
        Returns:
            The updated comment
            
        Raises:
            KeyError: If any of the comments don't exist
        """
        if comment_id not in self.comments:
            raise KeyError(f"Comment {comment_id} not found")
            
        # Verify all related comments exist
        for related_id in related_comment_ids:
            if related_id not in self.comments:
                raise KeyError(f"Related comment {related_id} not found")
        
        comment = self.comments[comment_id]
        comment.related_comment_ids = related_comment_ids
        comment.updated_at = datetime.now()
        
        return comment 