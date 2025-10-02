# SoraCleaner-Sora2 Video Watermark Remover

[中文版](./README_CN.md)

A powerful tool for removing watermarks from videos using AI-powered inpainting technology. The tool automatically detects video orientation (landscape/portrait) and applies appropriate watermark removal configurations.

## Features

- **Multi-Watermark Removal**: Remove multiple watermarks from a single video
- **Auto Orientation Detection**: Automatically detects landscape/portrait orientation and uses appropriate watermark positions
- **Audio Preservation**: Maintains original audio track in processed videos
- **Batch Processing**: Process entire directories of videos
- **AI-Powered Inpainting**: Uses STTN (Spatio-Temporal Transformer Network) for seamless watermark removal

## Requirements

- Python >= 3.12
- FFmpeg and FFprobe installed and available in PATH
- CUDA-compatible GPU (recommended for faster processing)

## Installation

1. Clone the repository with submodules:

```bash
git clone https://github.com/zstar1003/SoraCleaner
cd SoraCleaner
```

2. Install dependencies:

```bash
uv sync
```

## Configuration

Edit `config.yaml` to configure watermark positions:

```yaml
watermark:
  positions_landscape:  # Watermark positions for landscape videos
    - [35, 585, 176, 638]   # Format: [xmin, ymin, xmax, ymax]
    - [30, 68, 179, 118]
    - [1112, 321, 1266, 367]
  positions_portrait:  # Watermark positions for portrait videos
    - [28, 1029, 175, 1091]
    - [538, 604, 685, 657]
    - [25, 79, 173, 136]
  ckpt_p: "./weights/sttn.pth"
  mask_expand: 30          # Pixels to expand mask beyond watermark
  neighbor_stride: 10      # Temporal stride for inpainting
```

### Finding Watermark Positions

1. Open your video in a video player or image editor
2. Note the pixel coordinates (x, y) of the watermark's top-left and bottom-right corners
3. Add the position as `[xmin, ymin, xmax, ymax]` to the appropriate configuration section

## Usage

### Process a Single Video

```bash
python main.py --input /path/to/video.mp4
```

### Process a Directory of Videos

```bash
python main.py --input /path/to/video/directory/
```

The tool will:

1. Automatically detect video orientation (landscape/portrait)
2. Select appropriate watermark positions from config
3. Extract frames from the video
4. Remove watermarks using AI inpainting
5. Recreate video with original audio
6. Save output as `{original_name}_output.mp4`

## How It Works

1. **Video Analysis**: Detects FPS and orientation (landscape/portrait)
2. **Frame Extraction**: Extracts all frames from the video
3. **Orientation Detection**: Determines if video is landscape (width >= height) or portrait
4. **Watermark Masking**: Creates masks for all configured watermark positions
5. **AI Inpainting**: Uses STTN model to fill masked areas naturally
6. **Video Reconstruction**: Combines processed frames with original audio

## Project Structure

```
.
├── config.yaml           # Configuration file
├── main.py              # Main entry point
├── modules/
│   ├── __init__.py
│   ├── erase.py         # Watermark removal logic
│   └── sttn.py          # STTN model implementation
├── utils/
│   ├── image_utils.py   # Image processing utilities
│   ├── logging_utils.py # Logging utilities
│   └── video_utils.py   # Video processing utilities
├── weights/             # Model weights directory
└── STTN/               # STTN submodule
```

## Troubleshooting

**FFmpeg not found**

- Ensure FFmpeg and FFprobe are installed and in your system PATH

**CUDA out of memory**

- Process shorter videos or reduce `neighbor_stride` in config
- Use CPU mode (slower but works without GPU)

**Watermarks not fully removed**

- Adjust watermark coordinates in config.yaml
- Increase `mask_expand` value for larger coverage

**Audio/video out of sync**

- Check that original video FPS is correctly detected
- Ensure FFmpeg is up to date

## License

This project is for educational and research purposes only.

## Acknowledgments

- [STTN](https://github.com/researchmm/STTN) - Spatio-Temporal Transformer Network for video inpainting
- [KLing-Video-WatermarkRemover-Enhancer](https://github.com/chenwr727/KLing-Video-WatermarkRemover-Enhancer) - The basic code of for the repo.
