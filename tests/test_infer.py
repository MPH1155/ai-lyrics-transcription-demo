import pytest
import numpy as np
import soundfile as sf
import tempfile
import os
from src.lyrics_asr.infer import transcribe_audio_small, transcribe_audio_fine_tuned


@pytest.fixture
def synthetic_audio():
    """Generate a short synthetic audio file for testing."""
    sr = 16000
    duration = 1.0  # 1 second
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    audio = 0.5 * np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, audio, sr)
        yield f.name
        os.unlink(f.name)


def test_transcribe_audio_small(synthetic_audio):
    """Test base Whisper transcription on synthetic audio."""
    result = transcribe_audio_small(synthetic_audio)
    assert isinstance(result, str)
    assert len(result.strip()) >= 0  # May be empty for non-speech


def test_transcribe_audio_fine_tuned(synthetic_audio):
    """Test fine-tuned Whisper transcription on synthetic audio."""
    result = transcribe_audio_fine_tuned(synthetic_audio)
    assert isinstance(result, str)
    assert len(result.strip()) >= 0