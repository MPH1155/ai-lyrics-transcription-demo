import whisper
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import librosa
import numpy as np
import os

FINETUNED_DEFAULT_REPO = "MPH1155/whisper-fine-tuned"
FINETUNED_LOCAL_DIR = "./models/whisper-small-finetuned"


def _resolve_finetuned_source():
    env_repo = os.getenv("FINETUNED_MODEL_ID", "").strip()
    if env_repo:
        return env_repo
    if os.path.isdir(FINETUNED_LOCAL_DIR):
        return FINETUNED_LOCAL_DIR
    return FINETUNED_DEFAULT_REPO

def transcribe_audio_small(audio_file_path: str) -> str:
    model = whisper.load_model("small")
    lyrics = model.transcribe(audio_file_path)
    return lyrics["text"]

def transcribe_audio_small_with_rows(audio_file_path: str) -> dict:
    model = whisper.load_model("small")

    return model.transcribe(audio_file_path)

def transcribe_audio_fine_tuned(audio_file_path: str) -> str:
    audio, sr = librosa.load(audio_file_path, sr=16000)

    # Increase overlap to reduce cutoffs
    chunk_length = 480000  # 30s
    # overlap = 96000        # 6s overlap
    overlap = 0
    audio_length = len(audio)

    chunks = []
    start = 0
    while start < audio_length:
        end = min(start + chunk_length, audio_length)
        chunks.append(audio[start:end])
        start += chunk_length - overlap

    source = _resolve_finetuned_source()
    finetuned_processor = WhisperProcessor.from_pretrained(source)
    finetuned_model = WhisperForConditionalGeneration.from_pretrained(source)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    finetuned_model = finetuned_model.to(device)

    full_transcription = []
    for chunk in chunks:
        if len(chunk) < chunk_length:
            chunk = np.pad(chunk, (0, chunk_length - len(chunk)))

        input_features = finetuned_processor(chunk, sr, return_tensors="pt").input_features.to(device)
        generated_ids = finetuned_model.generate(
            input_features=input_features,
            no_repeat_ngram_size=8,
            max_length=448
        )
        transcription = finetuned_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        full_transcription.append(transcription.strip())

    return " ".join(full_transcription)