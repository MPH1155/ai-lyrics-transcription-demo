# Training and Evaluation Scripts

This directory contains scripts for fine-tuning and evaluating the Whisper model. These are **optional** for the demo deployment but included for reproducibility.

## Scripts

### training.py
Fine-tunes the Whisper model on a lyrics dataset.

**Usage:**
```bash
python training.py
```

### eval_with_HGFdata.py
Evaluates WER on a public Hugging Face dataset.

**Usage:**
```bash
python eval_with_HGFdata.py
```

### eval_with_full_song_data.py
Evaluates WER on the full custom dataset.

**Usage:**
```bash
python eval_with_full_song_data.py
```

### create_dataset.py
Creates a dataset CSV from audio files and lyrics.

**Usage:**
```bash
python create_dataset.py
```

### upload_dataset.py
Uploads the dataset to Hugging Face Hub.

**Usage:**
```bash
python upload_dataset.py
```

### song_downloader.py
Downloads songs from YouTube for dataset creation.

**Usage:**
```bash
python song_downloader.py
```

## Note
These scripts are **not required** for running the demo app. They are kept for:
- Reproducibility of training process
- Evaluation benchmarking
- Dataset creation documentation

If you only need the demo, you can safely ignore or delete these files.