# Deployment Guide

## 🚀 GitHub Pages (Static Frontend)

1. **Push to GitHub**:
```bash
git init
git add .
git commit -m "Initial commit: Whisper lyrics transcription demo"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/whisper-lyrics-demo.git
git push -u origin main
```

2. **Enable GitHub Pages**:
   - Go to repository Settings > Pages
   - Source: Deploy from branch
   - Branch: `main`, Folder: `/docs`
   - Save

3. **Update URLs** in `docs/index.html`:
   - Replace `YOUR_USERNAME` with your GitHub username
   - Replace `YOUR_VIDEO_ID` with your demo video ID
   - Update Hugging Face Space URL once created

Your static site will be live at: `https://YOUR_USERNAME.github.io/whisper-lyrics-demo/`

---

## 🤗 Hugging Face Spaces (Live Demo)

### Prerequisites
- Hugging Face account
- Git LFS installed: `git lfs install`

### Deploy Steps

1. **Create a new Space**:
   - Go to https://huggingface.co/new-space
   - Name: `whisper-lyrics-demo`
   - License: MIT
   - SDK: Docker
   - Hardware: CPU Basic (upgrade to GPU if needed for faster processing)

2. **Clone your Space**:
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/whisper-lyrics-demo
cd whisper-lyrics-demo
```

3. **Copy essential files**:
```bash
# From your project directory
cp app.py whisper-lyrics-demo/
cp vocal_seperator.py whisper-lyrics-demo/
cp requirements.txt whisper-lyrics-demo/
cp Dockerfile whisper-lyrics-demo/
cp -r src whisper-lyrics-demo/
cp .env.example whisper-lyrics-demo/
```

4. **Create README.md for Space**:
```markdown
---
title: Whisper Lyrics Transcription
emoji: 🎵
colorFrom: purple
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# 🎵 Whisper Lyrics Transcription

Upload an audio file and extract song lyrics using AI! This demo uses:
- Fine-tuned Whisper model for lyrics transcription
- Automatic vocal separation
- Side-by-side comparison (base vs fine-tuned)

## How to Use
1. Upload an audio file (.mp3, .wav, .m4a)
2. Wait for processing (vocal separation + transcription)
3. View results: original audio, separated vocals, and lyrics

**Processing time**: ~30-60s for a 30s clip (on CPU)

For more details, visit the [GitHub repository](https://github.com/YOUR_USERNAME/whisper-lyrics-demo).
```

5. **Add .gitignore for Space**:
```bash
cat > .gitignore << EOF
__pycache__/
*.pyc
.env
user_output/
user_uploaded_files/
models/*.safetensors
EOF
```

6. **Commit and push**:
```bash
git add .
git commit -m "Initial Space deployment"
git push
```

7. **Wait for build**: Check build logs at `https://huggingface.co/spaces/YOUR_USERNAME/whisper-lyrics-demo`

### Environment Variables (Optional)

If you need to set secrets (e.g., for model downloads):
- Go to Space Settings > Variables and secrets
- Add `FINETUNED_MODEL_ID` if using a private model
- Add `HF_TOKEN` if needed for private resources

---

## 🔧 Troubleshooting

### Docker Build Fails
- Check logs in HF Space build output
- Ensure all dependencies in `requirements.txt` are compatible
- Try locally: `docker build -t whisper-demo .`

### App Not Loading
- Check port is 7860 (required by HF Spaces)
- Verify `CMD` in Dockerfile uses `--host 0.0.0.0`
- Check Space logs for runtime errors

### Slow Processing
- Upgrade to GPU hardware in Space settings
- Reduce audio chunk size in `src/lyrics_asr/infer.py`
- Consider using quantized models

### Model Download Issues
- Set `FINETUNED_MODEL_ID` to public model repo
- Or include model files in repo (if license allows and size < 5GB)
- Use HF cache efficiently: `HF_HOME=/root/.cache/huggingface`

---

## 📹 Creating Demo Video

Recommended tools:
- **Loom** (loom.com) - Easy screen recording with narration
- **OBS Studio** - Free, professional recording
- **Windows Game Bar** - Built-in (Win+G)

What to show:
1. Landing page overview
2. Upload an audio file
3. Processing stages (vocal separation, transcription)
4. Results page with playback and lyrics
5. Compare base vs fine-tuned outputs

Tips:
- Keep it under 2 minutes
- Use a recognizable song (30s clip)
- Show the UI clearly at 1080p
- Add captions/annotations if needed

Upload to YouTube (unlisted) and embed in `docs/index.html`.

---

## 🔄 Updating Your Deployment

### GitHub Pages
```bash
# Make changes to docs/index.html or screenshots
git add docs/
git commit -m "Update demo page"
git push
```

### Hugging Face Space
```bash
cd whisper-lyrics-demo  # Your Space repo
# Make changes
git add .
git commit -m "Update: [describe changes]"
git push
```

Space will automatically rebuild and redeploy.

---

## 🌐 Custom Domain (Optional)

### GitHub Pages
- Add CNAME file in `docs/`: `echo "yourdomain.com" > docs/CNAME`
- Configure DNS: Add CNAME record pointing to `YOUR_USERNAME.github.io`

### Hugging Face Space
- Spaces don't support custom domains directly
- Use a reverse proxy (Cloudflare, Nginx) if needed

---

## 📊 Analytics (Optional)

Add Google Analytics to `docs/index.html`:
```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

Track Space usage via HF dashboard (coming soon).
