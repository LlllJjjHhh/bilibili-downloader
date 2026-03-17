# Bilibili Downloader

A simple Python script to download videos from Bilibili.

## Features

- 📥 Download single video by URL
- 📦 Batch download from text file (one URL per line)
- 🎬 Choose quality (from highest to lowest available)
- 🎵 Extract audio only (MP3 format)
- 🍪 Support cookie file for downloading high quality/VIP videos
- 💾 Save to custom output directory
- 📋 Download danmaku (optional)
- 🔍 Debug mode for troubleshooting
- ✅ Better error handling and progress reporting

## Requirements

- Python 3.7+
- you-get (automatically installed if not present)

## Installation

```bash
git clone https://github.com/LlllJjjHhh/bilibili-downloader.git
cd bilibili-downloader
pip install -r requirements.txt
```

## Usage

### Single video download

```bash
python download.py https://www.bilibili.com/video/BV1xx411c7mD
```

### Interactive mode

```bash
python download.py
# Then enter the Bilibili URL when prompted
```

### Batch download from file

Create a text file with one URL per line:
```txt
# urls.txt
https://www.bilibili.com/video/BV1xx411c7mD
https://www.bilibili.com/video/BV1sE411W7Af
```

Then run:
```bash
python download.py --batch-file urls.txt -o ./downloads
# Or directly:
python download.py urls.txt -o ./downloads
```

### Download audio only (mp3)

```bash
python download.py https://www.bilibili.com/video/BV1xx411c7mD --audio-only
```

### Choose quality

```bash
python download.py https://www.bilibili.com/video/BV1xx411c7mD -q 1080p
```

Available quality options: 1080p, 720p, 480p, 360p etc.

### Python API

```python
from bilibili_downloader import BilibiliDownloader

# Initialize with optional cookie file
downloader = BilibiliDownloader(cookie_file="./cookies.txt")

# Single download
success, error = downloader.download_single(
    "https://www.bilibili.com/video/BV1xx411c7mD",
    output_dir="./downloads",
    quality="1080p",
    download_danmaku=True,
    audio_only=False
)

# Batch download
urls = [
    "https://www.bilibili.com/video/BV1xx411c7mD",
    "https://www.bilibili.com/video/BV1sE411W7Af"
]
success_count, failed_count, failed_urls = downloader.download_batch(
    urls,
    output_dir="./downloads"
)

# Download from file
success_count, failed_count, failed_urls = downloader.download_from_file(
    "urls.txt",
    output_dir="./downloads"
)
```

## Options

```
usage: download.py [-h] [-o OUTPUT] [-q QUALITY] [--no-danmaku] [--audio-only]
                   [--batch-file BATCH_FILE] [--cookie COOKIE] [--debug] [url]

Bilibili Video Downloader

positional arguments:
  url              Bilibili video URL or path to url list file

optional arguments:
  -h, --help           show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory
  -q QUALITY, --quality QUALITY
                        Preferred quality (e.g. 1080p, 720p, 480p, 360p)
  --no-danmaku          Don't download danmaku
  --audio-only          Extract audio only (mp3)
  --batch-file BATCH_FILE
                        Batch download from text file (one URL per line)
  --cookie COOKIE       Path to cookie file for downloading high quality videos
  --debug               Enable debug output
```

## How to get cookie file

For downloading high quality videos that require login, you need to export cookies from your browser:

1. Install a cookie export extension like "Get Cookies.txt LOCALLY"
2. Log in to bilibili.com in your browser
3. Export cookies for bilibili.com to a text file
4. Use `--cookie` option to specify the cookie file:
   ```bash
   python download.py --cookie cookies.txt https://www.bilibili.com/video/BV1xx411c7mD
   ```

## Notes

- This tool is for personal use only. Please respect copyright laws.
- This project uses [you-get](https://github.com/soimort/you-get) as the backend.

## License

MIT

---

If this project helped you, buy me a coffee ☕

<img src="Qrcode.jpg" alt="Buy Me A Coffee" width="300">
