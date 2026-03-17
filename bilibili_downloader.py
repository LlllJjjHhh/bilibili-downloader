#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
from typing import Optional, List, Tuple


class BilibiliDownloader:
    """Simple Bilibili video downloader based on you-get"""
    
    def __init__(self, cookie_file: Optional[str] = None):
        self.cookie_file = cookie_file
        self.check_dependency()
    
    def check_dependency(self):
        """Check if you-get is installed"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "you_get", "--version"], 
                capture_output=True, 
                check=True
            )
            print(f"✅ Found you-get version: {result.stdout.decode().strip()}")
        except subprocess.CalledProcessError:
            print("⚠️  you-get not found. Installing...")
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "you-get"], 
                    check=True,
                    capture_output=False
                )
                print("✅ you-get installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install you-get: {e}")
                print("Please install manually: pip install you-get")
                sys.exit(1)
        except FileNotFoundError:
            print("❌ pip not found. Please check your Python installation")
            sys.exit(1)
    
    def _build_command(
        self,
        url: str,
        output_dir: Optional[str] = None,
        quality: Optional[str] = None,
        download_danmaku: bool = True,
        audio_only: bool = False,
        debug: bool = False
    ) -> List[str]:
        """Build the you-get command"""
        cmd = [sys.executable, "-m", "you_get"]
        
        if self.cookie_file:
            if os.path.exists(self.cookie_file):
                cmd.extend(["--cookies", self.cookie_file])
            else:
                print(f"⚠️  Cookie file {self.cookie_file} not found, ignoring...")
        
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            cmd.extend(["-o", output_dir])
        
        if quality:
            cmd.extend(["-q", quality])
        
        if not download_danmaku:
            cmd.append("--no-danmaku")
        
        if audio_only:
            cmd.append("--extract-audio")
            cmd.append("--audio-format")
            cmd.append("mp3")
        
        if debug:
            cmd.append("--debug")
        
        cmd.append(url)
        return cmd
    
    def download_single(
        self,
        url: str,
        output_dir: Optional[str] = None,
        quality: Optional[str] = None,
        download_danmaku: bool = True,
        audio_only: bool = False,
        debug: bool = False
    ) -> Tuple[bool, str]:
        """
        Download a single Bilibili video
        
        Args:
            url: Bilibili video URL
            output_dir: Output directory
            quality: Preferred quality (e.g. '1080p')
            download_danmaku: Whether to download danmaku
            audio_only: Extract audio only (mp3)
            debug: Enable debug output
        
        Returns:
            Tuple of (success: bool, error_message: str)
        """
        if not url.strip():
            return False, "URL is empty"
        
        # Validate URL
        if not ("bilibili.com" in url or "b23.tv" in url):
            return False, f"Invalid Bilibili URL: {url}"
        
        cmd = self._build_command(
            url, output_dir, quality, download_danmaku, audio_only, debug
        )
        
        print(f"🚀 Starting download: {url}")
        print(f"Command: {' '.join(cmd)}")
        print("-" * 60)
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=False)
            print("-" * 60)
            print(f"✅ Download completed: {url}")
            return True, ""
        except subprocess.CalledProcessError as e:
            error_msg = f"Download failed with exit code {e.returncode}"
            print("-" * 60)
            print(f"❌ {error_msg}")
            return False, error_msg
        except KeyboardInterrupt:
            print("\n⏹️  Download interrupted by user")
            return False, "Interrupted by user"
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def download_batch(
        self,
        urls: List[str],
        output_dir: Optional[str] = None,
        quality: Optional[str] = None,
        download_danmaku: bool = True,
        audio_only: bool = False,
        debug: bool = False
    ) -> Tuple[int, int, List[str]]:
        """
        Download multiple videos
        
        Returns:
            Tuple of (success_count, failed_count, failed_urls)
        """
        success_count = 0
        failed_count = 0
        failed_urls = []
        
        total = len(urls)
        print(f"📦 Batch downloading {total} URLs...")
        
        for i, url in enumerate(urls, 1):
            url = url.strip()
            if not url or url.startswith('#'):
                continue
                
            print(f"\n[{i}/{total}] Processing: {url}")
            success, error = self.download_single(
                url, output_dir, quality, download_danmaku, audio_only, debug
            )
            
            if success:
                success_count += 1
            else:
                failed_count += 1
                failed_urls.append((url, error))
        
        print("\n" + "=" * 60)
        print(f"📊 Batch download complete: {success_count} succeeded, {failed_count} failed")
        print("=" * 60)
        
        if failed_urls:
            print("\nFailed URLs:")
            for url, error in failed_urls:
                print(f"  - {url}: {error}")
        
        return success_count, failed_count, [u for u, _ in failed_urls]
    
    def download_from_file(
        self,
        file_path: str,
        output_dir: Optional[str] = None,
        quality: Optional[str] = None,
        download_danmaku: bool = True,
        audio_only: bool = False,
        debug: bool = False
    ) -> Tuple[int, int, List[str]]:
        """Download URLs from a text file, one URL per line"""
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return 0, 0, []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        
        return self.download_batch(
            urls, output_dir, quality, download_danmaku, audio_only, debug
        )


def main():
    parser = argparse.ArgumentParser(description='Bilibili Video Downloader')
    parser.add_argument('url', nargs='?', help='Bilibili video URL or path to url list file')
    parser.add_argument('-o', '--output', help='Output directory')
    parser.add_argument('-q', '--quality', help='Preferred quality (e.g. 1080p, 720p, 480p, 360p)')
    parser.add_argument('--no-danmaku', action='store_true', help="Don't download danmaku")
    parser.add_argument('--audio-only', action='store_true', help='Extract audio only (mp3)')
    parser.add_argument('--batch-file', help='Batch download from text file (one URL per line)')
    parser.add_argument('--cookie', help='Path to cookie file for downloading high quality videos')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    # Handle interactive mode
    if not args.url and not args.batch_file:
        url = input("Enter Bilibili video URL: ").strip()
        if not url:
            print("❌ URL is required")
            sys.exit(1)
        args.url = url
    
    downloader = BilibiliDownloader(cookie_file=args.cookie)
    
    if args.batch_file:
        # Batch download from file
        downloader.download_from_file(
            args.batch_file,
            output_dir=args.output,
            quality=args.quality,
            download_danmaku=not args.no_danmaku,
            audio_only=args.audio_only,
            debug=args.debug
        )
    elif args.url and os.path.isfile(args.url):
        # If input is a file, treat as batch file
        print(f"📖 Reading URLs from file: {args.url}")
        downloader.download_from_file(
            args.url,
            output_dir=args.output,
            quality=args.quality,
            download_danmaku=not args.no_danmaku,
            audio_only=args.audio_only,
            debug=args.debug
        )
    else:
        # Single download
        success, error = downloader.download_single(
            args.url,
            output_dir=args.output,
            quality=args.quality,
            download_danmaku=not args.no_danmaku,
            audio_only=args.audio_only,
            debug=args.debug
        )
        if not success:
            sys.exit(1)


if __name__ == "__main__":
    main()
