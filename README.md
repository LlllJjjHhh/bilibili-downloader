# Bilibili Downloader

A simple Python script to download videos from Bilibili.

## Features

- 📥 Download single video by URL
- 🎬 Choose quality (from highest to lowest available)
- 💾 Save to local file
- 📋 Download danmaku (optional)

## Requirements

- Python 3.7+
- you-get

## Installation

```bash
git clone https://github.com/luojianghao/bilibili-downloader.git
cd bilibili-downloader
pip install -r requirements.txt
```

## Usage

### Command line

```bash
python download.py https://www.bilibili.com/video/BV1xx411c7mD
```

### Python API

```python
from bilibili_downloader import BilibiliDownloader

downloader = BilibiliDownloader()
downloader.download("https://www.bilibili.com/video/BV1xx411c7mD")
```

### Interactive mode

```bash
python download.py
# Then enter the Bilibili URL when prompted
```

## Options

```
usage: download.py [-h] [-o OUTPUT] [-q QUALITY] [--no-danmaku] [url]

positional arguments:
  url              Bilibili video URL

optional arguments:
  -h, --help       show this help message and exit
  -o OUTPUT        Output directory
  -q QUALITY       Preferred quality (e.g. 1080p)
  --no-danmaku     Don't download danmaku
```

## Notes

- This tool is for personal use only. Please respect copyright laws.
- For some videos with high quality, you need to be logged in. Check you-get documentation for how to set cookies.

## License

MIT

---

If this project helped you, buy me a coffee ☕

<img src="Qrcode.jpg" alt="Buy Me A Coffee" width="300">
