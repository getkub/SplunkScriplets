# Animate Still Images into Motion Video — macOS Guide

This guide shows how to **animate still images** into motion videos using **Stable Video Diffusion (SVD)** on macOS. It is fully local and does **not require LLMs or MoneyPrinterTurbo**.

---

## Prerequisites

- macOS 11.0+ (Intel or Apple Silicon)
- Python 3.10+ installed
- Homebrew installed
- Optional: GPU (Apple M1/M2/M3) for faster generation

---

## 1) Install Homebrew Dependencies

Open Terminal and run:

```bash
brew update
brew install git ffmpeg
```

- `git` → for cloning models or scripts
- `ffmpeg` → for stitching frames into video

---

## 2) Create Python Environment

```bash
python3 -m venv svd-env
source svd-env/bin/activate
pip install --upgrade pip
```

---

## 3) Install Python Packages

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install diffusers transformers accelerate safetensors
pip install opencv-python imageio imageio-ffmpeg
```

> PyTorch auto-detects MPS on Apple Silicon to use GPU.

---

## 4) Download Stable Video Diffusion Model

```bash
# Pull the model from Hugging Face (first time downloads ~4GB)
# Replace with desired model if needed
from diffusers import StableVideoDiffusionPipeline
```

Or simply use it in your Python script (see next section).

---

## 5) Python Script to Animate Images

Create `animate_images.py`:

```python
import torch
from diffusers import StableVideoDiffusionPipeline
from PIL import Image
import imageio

# Load model
pipe = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid",
    torch_dtype=torch.float16,
    variant="fp16"
)
pipe = pipe.to("mps")  # use Apple GPU

# Load image
image = Image.open("my_image.jpg").convert("RGB")

# Generate motion frames
frames = pipe(image, num_frames=25).frames  # 25 frames ≈ 1 second at 25fps

# Save as mp4
video_path = "output.mp4"
imageio.mimsave(video_path, frames, fps=25)
print("Saved:", video_path)
```

Run:
```bash
python animate_images.py
```

You should get `output.mp4` with the animated motion of your still image.

---

## 6) Batch Processing Multiple Images (Optional)

You can loop through all images in a folder:

```python
import os
folder = "images/"
for file in os.listdir(folder):
    if file.endswith((".jpg", ".png")):
        # load, animate, save each image as shown above
```

---

## 7) Stitch Clips Together (Optional)

Use `ffmpeg`:
```bash
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[out]" -map "[out]" final.mp4
```

---

## Notes

- Fully local, free, no OpenAI or API keys needed.
- Works with Apple Silicon GPU via MPS.
- Adjust `num_frames` for longer/shorter clips.
- For higher quality, use more frames or higher-res images.

---

## References

- Hugging Face Stable Video Diffusion: https://huggingface.co/stabilityai/stable-video-diffusion-img2vid
- PyTorch MPS docs: https://pytorch.org/docs/stable/notes/mps.html
- Imageio for video writing: https://imageio.readthedocs.io/
