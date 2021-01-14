from pathlib import Path

import pytest


@pytest.fixture(scope='package')
def test_data() -> Path:
    """Test data directory."""
    return Path(__file__).parent / 'data'
