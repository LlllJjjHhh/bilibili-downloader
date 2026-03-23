#!/usr/bin/env python3
"""
Bilibili Downloader - Easy download Bilibili videos
"""
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bilibili_downloader import main

if __name__ == "__main__":
    main()
