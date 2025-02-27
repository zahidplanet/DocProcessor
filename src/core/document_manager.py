"""
Core functionality for managing documents.
"""

import os
import uuid
import shutil
from datetime import datetime
from typing import List, Dict, Optional, BinaryIO

from src.models.document import Document, DocumentType, DocumentStatus
from src.utils.document_processor import get_processor_for_file


class DocumentManager:
    """Manager for documents in the system."""
    
    def __init__(self, storage_dir: str):
        """
        Initialize the document manager.
        
        Args:
            storage_dir: Directory to store uploaded documents
        """
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        
        # In a real application, this would connect to a database
        self.documents: Dict[str, Document] = {}
    
    def upload_document(self, file_obj: BinaryIO, original_filename: str, 
                        document_type: DocumentType) -> Document:
        """
        Upload a new document.
        
        Args:
            file_obj: File object to upload
            original_filename: Original name of the file
            document_type: Type of document
            
        Returns:
            The newly created document
        """
        document_id = str(uuid.uuid4())
        _, ext = os.path.splitext(original_filename)
        filename = f"{document_id}{ext}"
        file_path = os.path.join(self.storage_dir, filename)
        
        # Save the file
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(file_obj, f)
        
        # Create document record
        document = Document(
            id=document_id,
            filename=filename,
            original_filename=original_filename,
            document_type=document_type,
            upload_date=datetime.now(),
            last_modified=datetime.now(),
            status=DocumentStatus.UPLOADED,
            version=1
        )
        
        self.documents[document_id] = document
        return document
    
    def get_document(self, document_id: str) -> Document:
        """
        Get a document by ID.
        
        Args:
            document_id: ID of the document to get
            
        Returns:
            The document
            
        Raises:
            KeyError: If the document doesn't exist
        """
        if document_id not in self.documents:
            raise KeyError(f"Document {document_id} not found")
            
        return self.documents[document_id]
    
    def get_document_text(self, document_id: str) -> str:
        """
        Extract text from a document.
        
        Args:
            document_id: ID of the document to extract text from
            
        Returns:
            Extracted text
            
        Raises:
            KeyError: If the document doesn't exist
        """
        document = self.get_document(document_id)
        file_path = os.path.join(self.storage_dir, document.filename)
        
        processor = get_processor_for_file(file_path)
        return processor.extract_text()
    
    def get_document_metadata(self, document_id: str) -> Dict:
        """
        Get metadata for a document.
        
        Args:
            document_id: ID of the document to get metadata for
            
        Returns:
            Document metadata
            
        Raises:
            KeyError: If the document doesn't exist
        """
        document = self.get_document(document_id)
        file_path = os.path.join(self.storage_dir, document.filename)
        
        processor = get_processor_for_file(file_path)
        return processor.get_metadata()
    
    def get_all_documents(self) -> List[Document]:
        """
        Get all documents.
        
        Returns:
            List of all documents
        """
        return list(self.documents.values())
    
    def update_document_status(self, document_id: str, status: DocumentStatus) -> Document:
        """
        Update the status of a document.
        
        Args:
            document_id: ID of the document to update
            status: New status of the document
            
        Returns:
            The updated document
            
        Raises:
            KeyError: If the document doesn't exist
        """
        document = self.get_document(document_id)
        document.status = status
        document.last_modified = datetime.now()
        
        return document
    
    def create_new_version(self, document_id: str, file_obj: BinaryIO) -> Document:
        """
        Create a new version of a document.
        
        Args:
            document_id: ID of the document to create a new version of
            file_obj: File object with the new version
            
        Returns:
            The newly created document version
            
        Raises:
            KeyError: If the document doesn't exist
        """
        original_document = self.get_document(document_id)
        
        new_document_id = str(uuid.uuid4())
        _, ext = os.path.splitext(original_document.filename)
        filename = f"{new_document_id}{ext}"
        file_path = os.path.join(self.storage_dir, filename)
        
        # Save the file
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(file_obj, f)
        
        # Create new document record
        new_document = Document(
            id=new_document_id,
            filename=filename,
            original_filename=original_document.original_filename,
            document_type=original_document.document_type,
            upload_date=datetime.now(),
            last_modified=datetime.now(),
            status=DocumentStatus.UPDATED,
            version=original_document.version + 1,
            parent_document_id=document_id
        )
        
        self.documents[new_document_id] = new_document
        return new_document
    
    def get_document_version_history(self, document_id: str) -> List[Document]:
        """
        Get the version history of a document.
        
        Args:
            document_id: ID of the document to get history for
            
        Returns:
            List of document versions, sorted by version number
            
        Raises:
            KeyError: If the document doesn't exist
        """
        document = self.get_document(document_id)
        
        # Find all versions of this document
        versions = [document]
        
        # Find all documents that have this as a parent
        for doc in self.documents.values():
            if doc.parent_document_id == document_id:
                versions.append(doc)
        
        # If this document has a parent, get its history too
        if document.parent_document_id:
            parent_versions = self.get_document_version_history(document.parent_document_id)
            versions.extend(parent_versions)
        
        # Sort by version number
        return sorted(versions, key=lambda d: d.version) 