# 🎵 Lyrics Transcription & Vocal Separation - AI-Powered Song Lyrics Extraction

[![Live Demo](https://img.shields.io/badge/🤗-Live_Demo-yellow)](https://huggingface.co/spaces/YOUR_USERNAME/whisper-lyrics-demo)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/YOUR_USERNAME/whisper-lyrics-demo)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> **Fine-tuned OpenAI Whisper model with automatic vocal separation for accurate song lyrics transcription. Compare base vs. fine-tuned performance in real-time.**

🌐 **[View Static Demo Page](https://YOUR_USERNAME.github.io/whisper-lyrics-demo/)** | 🚀 **[Try Live Demo on HF Spaces](https://huggingface.co/spaces/YOUR_USERNAME/whisper-lyrics-demo)**

![Demo Preview](docs/screenshots/results.png)

## ✨ Features

- 🧠 **Fine-Tuned Whisper Model**: Custom-trained on 100+ song lyrics for superior music transcription accuracy
- 🎤 **Automatic Vocal Separation**: Isolates vocals using audio-separator before transcription
- 📊 **Side-by-Side Comparison**: View base Whisper vs. fine-tuned model outputs (segmented + full)
- 🎨 **Modern Web UI**: Clean Bootstrap 5 interface with audio playback
- ⚡ **FastAPI Backend**: Efficient async processing with CORS support
- 🐳 **Docker Ready**: Deploy anywhere with included Dockerfile

## 🎯 Quick Start

### Prerequisites
- Python 3.10+
- FFmpeg (for audio processing)
- 4GB+ RAM (8GB recommended)

### Local Setup
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/whisper-lyrics-demo.git
cd whisper-lyrics-demo

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn app:app --host 127.0.0.1 --port 8000

# Open http://127.0.0.1:8000 in your browser
```

## 📸 Screenshots

<table>
  <tr>
    <td><img src="docs/screenshots/upload.png" alt="Upload Interface" width="400"/></td>
  </tr>
  <tr>
    <td colspan="2"><img src="docs/screenshots/results.png" alt="Results Page" width="800"/></td>
  </tr>
</table>

## 🏗️ Architecture

```mermaid
graph LR
    A[User Upload] --> B[Vocal Separation]
    B --> C[Whisper Base]
    B --> D[Whisper Fine-tuned]
    C --> E[Results Display]
    D --> E
    B --> F[Audio Playback]
    F --> E
```

## 2. Current Repository Status
This is an in-progress cleanup. Planned refactor will move ad-hoc scripts into a package structure under `src/` with a unified CLI. See `Roadmap` below.

## 3. Directory Overview (current state)
```
project/
  training.py                # Fine-tuning script
  eval_with_HGFdata.py       # WER evaluation on public dataset
  eval_with_full_song_data.py# WER eval on combined custom splits
  web_app.py                 # FastAPI demo (upload -> separate -> transcribe)
  vocal_seperator.py         # Uses audio-separator lib
  lyrics_transcripter.py     # Functions for base + fine-tuned transcription
  create_dataset.py          # Build CSV from raw audio + lyrics
  upload_dataset.py          # Push dataset to HF Hub
  huggingface_api.py         # (Will be removed) contains hard-coded tokens
  requirements.txt
  .gitignore
  README.md
  data/                      # (ignored) working audio
  original_data/             # (ignored) raw collected dataset
  whisper-finetuned/         # (ignored) fine-tuned model artifacts
  logs/                      # training logs (ignored)
```

## 4. Installation
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Hugging Face Authentication
Do NOT hardcode tokens. Export environment variables instead:
```bash
# PowerShell
$Env:HUGGINGFACE_TOKEN = "hf_xxx"
```
Then inside Python:
```python
from huggingface_hub import login
import os
login(token=os.getenv("HUGGINGFACE_TOKEN"))
```

## 6. Training
```bash
python training.py
```
Outputs:
- Fine-tuned model directory: `./whisper-finetuned/`
- Logs in `./logs/`
- (Optional) Pushed model to Hub (configure push_to_hub)

## 7. Evaluation (WER)
Public dataset example:
```bash
python eval_with_HGFdata.py
```
Custom combined dataset example:
```bash
python eval_with_full_song_data.py
```

## 8. FastAPI Demo (Local)
```bash
uvicorn web_app:app --reload --port 8000
```
Open: http://localhost:8000

## 9. Deployment Options
### Option A: Hugging Face Spaces (Recommended for ML demo)
- Framework: Gradio or FastAPI Space
- Pros: GPU availability, simple model loading.
- Action: Wrap logic into a `app.py` Gradio interface or keep FastAPI and define `space_runtime.txt`.

### Option B: Vercel + Inference Backend
Vercel cannot run heavy GPU inference directly. Strategy:
1. Host inference API elsewhere (Render, HF Inference Endpoints, Replicate, or a lightweight EC2/GCP instance).
2. Create a separate `frontend/` (Next.js) deployed to Vercel.
3. Frontend calls backend REST endpoints: `/separate`, `/transcribe/base`, `/transcribe/fine`.
4. Optionally stream transcription progress via Server-Sent Events or websockets.

### Option C: All-in-one on a GPU VM
Use Docker + Nginx + systemd. Overkill for a portfolio demo unless you want DevOps credit.

## 10. Suggested Refactor (Target Structure)
```
.
├─ src/lyrics_asr/
│  ├─ __init__.py
│  ├─ data.py              # dataset prep / HF loading
│  ├─ train.py             # train entry (function)
│  ├─ eval.py              # compute WER
│  ├─ infer.py             # chunked transcription utilities
│  ├─ separate.py          # vocal separation wrapper
│  ├─ cli.py               # unified CLI (train/eval/infer)
│  └─ config.py            # load YAML config
├─ configs/
│  ├─ train.yaml
│  ├─ eval.yaml
│  └─ infer.yaml
├─ scripts/
│  ├─ download_dataset.ps1
│  └─ prepare_data.ps1
├─ tests/
│  ├─ test_infer.py
│  └─ fixtures/
```
Planned improvements: remove duplicated logic, centralize device selection, use argparse or Typer.

## 11. Security & Secrets
- Remove `huggingface_api.py` (currently contains a token!)
- Use `.env` with `python-dotenv` OR environment variables
- Never commit model weights if license forbids or they are large.

## 12. Roadmap
- [ ] Migrate scripts into `src/lyrics_asr`
- [ ] Introduce config-driven pipeline
- [ ] Add tests + CI workflow (GitHub Actions)
- [ ] Add small sample audio + smoke test
- [ ] Publish model + dataset cards on Hugging Face Hub
- [ ] Build Next.js frontend (optional) + deploy to Vercel
- [ ] Add Gradio demo for Spaces

## 13. Evaluation Metrics Snapshot (example)
| Model | WER (eval set) |
|-------|----------------|
| Base Whisper Small | TBD |
| Fine-tuned | TBD |
| Improvement | TBD |

## 14. Contributing (Future)
Style: black + ruff
Tests: pytest
Environment: Python 3.10+

## 15. License
Choose a license (MIT recommended for portfolio) and add a `LICENSE` file.

---
Questions / feedback welcome. This README will evolve with the refactor.
