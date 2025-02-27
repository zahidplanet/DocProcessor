"""
Test cases for the DocProcessor application.
"""

import os
import pytest
import tempfile
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
    
    with app.test_client() as client:
        yield client


def test_index_page(client):
    """Test that the index page loads."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'DocProcessor Dashboard' in response.data


def test_documents_page(client):
    """Test that the documents page loads."""
    response = client.get('/documents')
    assert response.status_code == 200
    assert b'Documents' in response.data


def test_upload_page(client):
    """Test that the upload page loads."""
    response = client.get('/upload')
    assert response.status_code == 200
    assert b'Upload Document' in response.data


def test_404_page(client):
    """Test the 404 error page."""
    response = client.get('/nonexistent')
    assert response.status_code == 404


def test_changelog_redirect(client):
    """Test that the changelog route redirects when no document exists."""
    response = client.get('/documents/nonexistent-id/changelog')
    assert response.status_code == 302  # Redirect
    assert b'Redirecting' in response.data 