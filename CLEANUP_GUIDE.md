# Files to Delete for Clean Repository

## Safe to Delete (Already in .gitignore)
These directories/files are already excluded from Git, but you can manually delete them to clean up:

### Large Data Directories
- `data/` - Working audio files
- `original_data/` - Raw dataset
- `youtube_download/` - Downloaded audio
- `user_uploaded_files/` - User uploads (runtime)
- `user_output/` - Processed outputs (runtime)
- `models/` - Model checkpoints (large)
- `whisper-fine-tuned/` - Fine-tuned model (already on HF Hub)

### Logs & Cache
- `logs/` - Training logs
- `graphs/` - Training graphs
- `__pycache__/` - Python cache
- `.pytest_cache/` - Pytest cache
- `.venv/` - Virtual environment (recreate with pip install)

### Temporary Files
- `archive.txt` - If not needed

## Files to Keep for Deployment

### Essential Application Files
- `app.py` - Main FastAPI app
- `vocal_seperator.py` - Vocal separation logic
- `src/lyrics_asr/` - Package code
- `requirements.txt` - Dependencies
- `Dockerfile` - For HF Spaces
- `space.yml` - HF Space config
- `.env.example` - Template for environment variables
- `.gitignore` - Git exclusions
- `LICENSE` - MIT license
- `README.md` - Project documentation
- `DEPLOYMENT.md` - Deployment guide
- `docs/` - GitHub Pages site

### Optional Files (Keep if You Want Reproducibility)
- `training.py` - Fine-tuning script
- `eval_with_HGFdata.py` - Evaluation script
- `eval_with_full_song_data.py` - Evaluation script
- `create_dataset.py` - Dataset creation
- `upload_dataset.py` - Upload to HF Hub
- `song_downloader.py` - Download songs
- `lyrics_transcripter.py` - Old transcription code (replaced by src/)

### Files to DELETE (Duplicates/Old Code)
- `huggingface_api.py` - ⚠️ Contains hardcoded token, replaced by env vars
- `lyrics_transcripter.py` - Replaced by `src/lyrics_asr/infer.py`

## PowerShell Commands to Clean Up

```powershell
# Navigate to project
cd d:\cuhk\IERG4320\project_2.0

# Delete large data directories (CAREFUL - make sure you have backups!)
Remove-Item -Recurse -Force data
Remove-Item -Recurse -Force original_data
Remove-Item -Recurse -Force youtube_download
Remove-Item -Recurse -Force user_uploaded_files
Remove-Item -Recurse -Force user_output
Remove-Item -Recurse -Force models
Remove-Item -Recurse -Force whisper-fine-tuned

# Delete logs and cache
Remove-Item -Recurse -Force logs
Remove-Item -Recurse -Force graphs
Remove-Item -Recurse -Force __pycache__
Remove-Item -Recurse -Force .pytest_cache

# Delete virtual environment (you can recreate it)
Remove-Item -Recurse -Force .venv

# Delete sensitive/old files
Remove-Item -Force huggingface_api.py
Remove-Item -Force archive.txt

# Optional: Delete training/eval scripts if not needed for portfolio
# Remove-Item -Force training.py
# Remove-Item -Force eval_with_HGFdata.py
# Remove-Item -Force eval_with_full_song_data.py
# Remove-Item -Force create_dataset.py
# Remove-Item -Force upload_dataset.py
# Remove-Item -Force song_downloader.py
# Remove-Item -Force lyrics_transcripter.py
```

## After Cleanup, Your Repo Should Look Like:

```
whisper-lyrics-demo/
├── app.py                   # Main application
├── vocal_seperator.py       # Vocal separation
├── requirements.txt         # Dependencies
├── Dockerfile              # HF Space deployment
├── space.yml               # HF Space config
├── .env.example            # Environment template
├── .gitignore              # Git exclusions
├── LICENSE                 # MIT license
├── README.md               # Documentation
├── DEPLOYMENT.md           # Deployment guide
├── src/
│   └── lyrics_asr/
│       ├── __init__.py
│       └── infer.py        # Transcription logic
├── docs/
│   ├── index.html          # GitHub Pages site
│   └── screenshots/        # UI screenshots
└── tests/                  # Unit tests (optional)
    ├── __init__.py
    ├── test_api.py
    └── test_infer.py
```

## Final Size Target
After cleanup: **< 50MB** (excluding screenshots)
Before cleanup: **~5GB+** with models/data

## Important Notes
1. ⚠️ **Backup first** if you need the data/models later
2. Models are on Hugging Face Hub - you don't need local copies
3. Runtime directories (user_output/, user_uploaded_files/) are created automatically by app.py
4. .venv can be recreated with `python -m venv .venv` and `pip install -r requirements.txt`
