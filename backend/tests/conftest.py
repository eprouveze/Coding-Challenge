import pytest
import os
import sys
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

@pytest.fixture
def test_settings():
    """Test settings fixture"""
    return {
        "DATABASE_URL": "sqlite:///./test.db",
        "SECRET_KEY": "test-secret-key",
        "DEBUG": True
    }

@pytest.fixture
def client():
    """Test client fixture"""
    try:
        from fastapi.testclient import TestClient
        from main import app
        return TestClient(app)
    except ImportError:
        pytest.skip("FastAPI or main app not available")