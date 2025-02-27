"""
Tests for the DocProcessor application.
"""

import os
import pytest
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_index(client):
    """Test the index page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to DocProcessor' in response.data


def test_documents_page(client):
    """Test the documents page."""
    response = client.get('/documents')
    assert response.status_code == 200
    assert b'Documents' in response.data


def test_upload_page(client):
    """Test the upload page."""
    response = client.get('/upload')
    assert response.status_code == 200
    assert b'Upload Document' in response.data


def test_error_404(client):
    """Test 404 error page."""
    response = client.get('/non-existent-page')
    assert response.status_code == 404
    assert b'Page Not Found' in response.data 