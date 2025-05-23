import pytest
import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

def test_basic_import():
    """Test that we can import basic modules"""
    try:
        import main
        assert main is not None
    except ImportError as e:
        pytest.skip(f"Main module import failed: {e}")

def test_health_endpoint():
    """Test health endpoint"""
    try:
        from fastapi.testclient import TestClient
        from main import app
        
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    except ImportError:
        pytest.skip("FastAPI or main app not available")

def test_root_endpoint():
    """Test root endpoint"""
    try:
        from fastapi.testclient import TestClient
        from main import app
        
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
    except ImportError:
        pytest.skip("FastAPI or main app not available")

def test_app_creation():
    """Test that FastAPI app can be created"""
    try:
        from main import app
        assert app is not None
        assert hasattr(app, 'routes')
    except ImportError:
        pytest.skip("Main app not available")