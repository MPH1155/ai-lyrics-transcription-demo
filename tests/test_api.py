import pytest
from fastapi.testclient import TestClient
from app import app
import numpy as np
import soundfile as sf
import tempfile
import os


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def synthetic_audio_file():
    """Generate a short synthetic audio file for API testing."""
    sr = 16000
    duration = 1.0
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    audio = 0.5 * np.sin(2 * np.pi * 440 * t)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, audio, sr)
        yield f.name
        os.unlink(f.name)


def test_health_check(client):
    """Test the /healthz endpoint."""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_transcribe(client, synthetic_audio_file):
    """Test the /api/transcribe endpoint with synthetic audio."""
    with open(synthetic_audio_file, "rb") as f:
        response = client.post("/api/transcribe", files={"file": ("test.wav", f, "audio/wav")})

    assert response.status_code == 200
    data = response.json()
    assert "filename" in data
    assert "base_transcript" in data
    assert "fine_tuned_transcript" in data
    assert "base_transcript_segmented" in data
    assert isinstance(data["base_transcript"], str)
    assert isinstance(data["fine_tuned_transcript"], str)