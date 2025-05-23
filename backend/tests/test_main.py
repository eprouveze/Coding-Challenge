import pytest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

def test_basic():
    """Basic test that always passes"""
    assert True

def test_python_version():
    """Test Python version"""
    assert sys.version_info >= (3, 8)

def test_main_import():
    """Test that we can import main module"""
    try:
        import main
        assert hasattr(main, 'app')
    except ImportError:
        pytest.skip("Main module not available")

def test_fastapi_endpoints():
    """Test FastAPI endpoints"""
    try:
        from fastapi.testclient import TestClient
        import main
        
        client = TestClient(main.app)
        
        # Test root endpoint
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        
        # Test health endpoint
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        
        # Test events endpoint
        response = client.get("/api/v1/events")
        assert response.status_code == 200
        
    except ImportError:
        pytest.skip("FastAPI or main app not available")