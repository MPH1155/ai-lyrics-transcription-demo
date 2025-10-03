from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import traceback
from typing import Optional

# Lazy imports for heavy modules
from src.lyrics_asr.infer import (
    transcribe_audio_small,
    transcribe_audio_fine_tuned,
    transcribe_audio_small_with_rows,
)

from vocal_seperator import seperate_vocals_instrumental

# Runtime directories
RUNTIME_DIRS = ["user_output", "user_uploaded_files"]
for d in RUNTIME_DIRS:
    os.makedirs(d, exist_ok=True)

app = FastAPI(title="Whisper Lyrics Demo", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/user_output", StaticFiles(directory="user_output"), name="user_output")
app.mount("/user_uploaded_files", StaticFiles(directory="user_uploaded_files"), name="user_uploaded_files")


def process_audio(file_path: str) -> Optional[str]:
    try:
        vocal_file_path = seperate_vocals_instrumental(file_path, "user_output/")
        return vocal_file_path
    except Exception:
        print("[WARN] Vocal separation failed:\n" + traceback.format_exc())
        return None


def get_lyrics(file_path: str):
    lyrics_finetuned = transcribe_audio_fine_tuned(file_path)
    lyrics_small = transcribe_audio_small(file_path)
    transcript = transcribe_audio_small_with_rows(file_path)
    lyrics_small_rows_seperated = "".join(seg["text"] + "\n" for seg in transcript.get("segments", []))
    return lyrics_small, lyrics_finetuned, lyrics_small_rows_seperated


@app.post("/api/transcribe")
async def api_transcribe(file: UploadFile = File(...), separate: bool = False):
    try:
        filename = file.filename.strip().replace(" ", "_")
        file_location = os.path.join("user_uploaded_files", filename)
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)

        vocal_path = process_audio(file_location) if separate else None
        target_for_transcription = vocal_path or file_location

        small, finetuned, small_rows = get_lyrics(target_for_transcription)

        return {
            "filename": filename,
            "used_vocals": bool(vocal_path),
            "vocals_path": f"/user_output/{os.path.basename(vocal_path)}" if vocal_path else None,
            "base_transcript": small,
            "fine_tuned_transcript": finetuned,
            "base_transcript_segmented": small_rows.strip(),
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "trace": traceback.format_exc()})


@app.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    filename = file.filename.strip().replace(" ", "_")
    file_location = f"user_uploaded_files/{filename}"
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    vocals_path = process_audio(file_location)
    lyrics_small, lyrics_finetuned, lyrics_small_rows_seperated = get_lyrics(file_location)
    vocals_filename = os.path.basename(vocals_path) if vocals_path else None
    lyrics_small_rows_seperated = lyrics_small_rows_seperated.replace("\n", "<br>")

    vocal_section = f"""
            <div class=\"card mb-4\">
                <div class=\"card-header\"><strong>Vocal Separation</strong></div>
                <div class=\"card-body text-center\">
                    <audio controls class=\"w-100\">
                        <source src=\"/user_output/{vocals_filename}\" type=\"audio/wav\">
                        Your browser does not support the audio element.
                    </audio>
                </div>
            </div>""" if vocals_filename else "<p class=\"text-muted\">Vocal separation failed, using original audio for transcription.</p>"

    html_content = f"""
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <title>Processed Audio</title>
        <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">
    </head>
    <body>
        <div class=\"container mt-5\">
            <h1 class=\"mb-4 text-center\">Processed Audio</h1>
            <div class=\"card mb-4\">
                <div class=\"card-header\"><strong>Original Uploaded Audio</strong></div>
                <div class=\"card-body text-center\">
                    <audio controls class=\"w-100\">
                        <source src=\"/user_uploaded_files/{filename}\" type=\"audio/wav\">
                        Your browser does not support the audio element.
                    </audio>
                </div>
            </div>
            {vocal_section}
            <div class=\"card mb-4\">
                <div class=\"card-header\"><strong>Lyrics (Base Whisper - Segmented)</strong></div>
                <div class=\"card-body\"><p>{lyrics_small_rows_seperated}</p></div>
            </div>
            <div class=\"card mb-4\">
                <div class=\"card-header\"><strong>Lyrics (Fine-Tuned)</strong></div>
                <div class=\"card-body\"><p>{lyrics_finetuned}</p></div>
            </div>
            <div class=\"card mb-4\">
                <div class=\"card-header\"><strong>Lyrics (Base Whisper - Single Line)</strong></div>
                <div class=\"card-body\"><p>{lyrics_small}</p></div>
            </div>
            <div class=\"text-center\"><a href=\"/\" class=\"btn btn-primary\">Upload Another File</a></div>
        </div>
        <script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js\"></script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/")
async def main():
    index = f"""
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <title>Upload Audio</title>
        <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">
    </head>
    <body>
        <div class=\"container mt-5\">
            <h1 class=\"mb-2 text-center\">Song Transcriber demo</h1>
            <p class=\"text-center text-muted\">Base vs Fine-Tuned • Vocal Separation • FastAPI Space</p>
            <div class=\"card\">
                <div class=\"card-body\">
                    <form action=\"/upload-audio/\" enctype=\"multipart/form-data\" method=\"post\">
                        <div class=\"mb-3\">
                            <label for=\"file\" class=\"form-label\">Choose Audio File (.mp3/.wav)</label>
                            <input class=\"form-control\" type=\"file\" id=\"file\" name=\"file\" required>
                        </div>
                        <div class=\"alert alert-info py-2\" style=\"font-size:0.85rem;\">Large files may take longer—start with a 10–30s clip.</div>
                        <div class=\"d-grid\">
                            <button type=\"submit\" class=\"btn btn-success\">Upload and Process</button>
                        </div>
                    </form>
                    <hr>
                </div>
            </div>
        </div>
        <script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js\"></script>
    </body>
    </html>
    """
    return HTMLResponse(content=index)


@app.get("/healthz")
async def health_check():
    return {"status": "ok"}