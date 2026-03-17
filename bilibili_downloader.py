#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
from typing import Optional


class BilibiliDownloader:
    """Simple Bilibili video downloader based on you-get"""
    
    def __init__(self):
        self.check_dependency()
    
    def check_dependency(self):
        """Check if you-get is installed"""
        try:
            subprocess.run([sys.executable, "-m", "you_get", "--version"], 
                         capture_output=True, check=True)
        except subprocess.CalledProcessError:
            print("⚠️  you-get not found. Installing...")
            subprocess.run([sys.executable, "-m", "pip", "install", "you-get"], check=True)
            print("✅ you-get installed successfully")
    
    def download(
        self,
        url: str,
        output_dir: Optional[str] = None,
        quality: Optional[str] = None,
        download_danmaku: bool = True
    ):
        """
        Download a Bilibili video
        
        Args:
            url: Bilibili video URL
            output_dir: Output directory
            quality: Preferred quality (e.g. '1080p')
            download_danmaku: Whether to download danmaku
        """
        cmd = [sys.executable, "-m", "you_get"]
        
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            cmd.extend(["-o", output_dir])
        
        if quality:
            cmd.extend(["-q", quality])
        
        if not download_danmaku:
            cmd.append("--no-danmaku")
        
        cmd.append(url)
        
        print(f"🚀 Starting download: {url}")
        print(f"Command: {' '.join(cmd)}")
        print("-" * 50)
        
        try:
            subprocess.run(cmd, check=True)
            print("-" * 50)
            print("✅ Download completed!")
        except subprocess.CalledProcessError as e:
            print("-" * 50)
            print(f"❌ Download failed with exit code {e.returncode}")
            raise


def main():
    parser = argparse.ArgumentParser(description='Bilibili Video Downloader')
    parser.add_argument('url', nargs='?', help='Bilibili video URL')
    parser.add_argument('-o', '--output', help='Output directory')
    parser.add_argument('-q', '--quality', help='Preferred quality (e.g. 1080p)')
    parser.add_argument('--no-danmaku', action='store_true', help="Don't download danmaku")
    
    args = parser.parse_args()
    
    url = args.url
    
    if not url:
        url = input("Enter Bilibili video URL: ").strip()
    
    if not url:
        print("❌ URL is required")
        sys.exit(1)
    
    downloader = BilibiliDownloader()
    downloader.download(
        url,
        output_dir=args.output,
        quality=args.quality,
        download_danmaku=not args.no_danmaku
    )


if __name__ == "__main__":
    main()
