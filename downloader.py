#!/usr/bin/env python3
"""
YouTube Video Downloader
Main downloader script using yt-dlp
"""

import os
import sys
import json
import argparse
from pathlib import Path
import subprocess

class YouTubeDownloader:
    def __init__(self, output_dir="./downloads", quality="2160p"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.quality = quality
        # Set defaults before loading config
        self.max_retries = 3
        self.audio_format = 'mp3'
        self.audio_quality = '320'
        self.load_config()
        
    def load_config(self):
        """Load configuration from config.json if exists"""
        config_file = Path("config.json")
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
                self.quality = config.get('default_quality', self.quality)
                self.output_dir = Path(config.get('download_folder', self.output_dir))
                self.max_retries = config.get('max_retries', self.max_retries)
                self.audio_format = config.get('audio_format', self.audio_format)
                self.audio_quality = str(config.get('audio_quality', self.audio_quality))
    
    def get_format_string(self, quality, audio_only=False):
        """Get yt-dlp format string based on quality"""
        if audio_only:
            return 'bestaudio/best'
        
        quality_map = {
            '2160p': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]/best',
            '1440p': 'bestvideo[height<=1440]+bestaudio/best[height<=1440]/best',
            '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/best',
            '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]/best',
            '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]/best',
            '360p': 'bestvideo[height<=360]+bestaudio/best[height<=360]/best',
        }
        
        return quality_map.get(quality, quality_map['1080p'])
    
    def download_single(self, url, audio_only=False):
        """Download a single video"""
        print(f"\n📥 Downloading: {url}")
        print(f"Quality: {self.quality if not audio_only else 'Audio Only'}")
        print(f"Output: {self.output_dir}")
        
        format_string = self.get_format_string(self.quality, audio_only)
        
        cmd = [
            'yt-dlp',
            '-f', format_string,
            '-o', str(self.output_dir / '%(title)s.%(ext)s'),
            '--no-overwrites',
            '--continue',
            '--ignore-errors',
            '--no-warnings',
            '--newline',
            '--merge-output-format', 'mp4',
            '--retries', str(self.max_retries),
        ]
        
        if audio_only:
            # Remove merge-output-format for audio
            cmd = [c for c in cmd if c not in ('--merge-output-format', 'mp4')]
            cmd.extend([
                '-x',
                '--audio-format', self.audio_format,
                '--audio-quality', self.audio_quality,
            ])
        
        cmd.append(url)
        
        try:
            subprocess.run(cmd, check=True)
            print("✅ Download completed!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Download failed: {e}")
            return False
        except KeyboardInterrupt:
            print("\n⚠️  Download cancelled by user")
            return False
    
    def download_bulk(self, file_path, audio_only=False):
        """Download multiple videos from a text file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and line.strip().startswith('http')]
        
        if not urls:
            print("❌ No valid URLs found in file")
            return
        
        print(f"\n📋 Found {len(urls)} URLs to download")
        print(f"Quality: {self.quality if not audio_only else 'Audio Only'}")
        print(f"Output: {self.output_dir}\n")
        
        success_count = 0
        failed_urls = []
        
        for i, url in enumerate(urls, 1):
            print(f"\n{'='*60}")
            print(f"Progress: {i}/{len(urls)}")
            print(f"{'='*60}")
            
            if self.download_single(url, audio_only):
                success_count += 1
            else:
                failed_urls.append(url)
        
        # Summary
        print(f"\n{'='*60}")
        print(f"📊 DOWNLOAD SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Successful: {success_count}/{len(urls)}")
        print(f"❌ Failed: {len(failed_urls)}/{len(urls)}")
        
        if failed_urls:
            print(f"\n❌ Failed URLs:")
            for url in failed_urls:
                print(f"  - {url}")
            
            # Save failed URLs to file
            failed_file = self.output_dir / 'failed_urls.txt'
            with open(failed_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(failed_urls))
            print(f"\n💾 Failed URLs saved to: {failed_file}")

def main():
    parser = argparse.ArgumentParser(
        description='YouTube Video Downloader - Download videos up to 1080p',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Download single video:
    python downloader.py --url "https://www.youtube.com/watch?v=VIDEO_ID"
  
  Bulk download from file:
    python downloader.py --file urls.txt
  
  Download audio only:
    python downloader.py --url "VIDEO_URL" --audio-only
  
  Specify quality:
    python downloader.py --url "VIDEO_URL" --quality 720p
        """
    )
    
    parser.add_argument('--url', help='YouTube video URL')
    parser.add_argument('--file', help='Text file with multiple URLs (one per line)')
    parser.add_argument('--quality', choices=['360p', '480p', '720p', '1080p', '1440p', '2160p'], 
                       default='1080p', help='Video quality (default: 1080p, supports up to 4K)')
    parser.add_argument('--audio-only', action='store_true', help='Download audio only (MP3)')
    parser.add_argument('--output', default='./downloads', help='Output directory (default: ./downloads)')
    
    args = parser.parse_args()
    
    # Check if yt-dlp is installed
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ yt-dlp is not installed!")
        print("Please run the installer script first:")
        print("  Windows: install.bat")
        print("  Linux/Mac: ./install.sh")
        sys.exit(1)
    
    if not args.url and not args.file:
        parser.print_help()
        sys.exit(1)
    
    downloader = YouTubeDownloader(output_dir=args.output, quality=args.quality)
    
    if args.url:
        downloader.download_single(args.url, args.audio_only)
    elif args.file:
        downloader.download_bulk(args.file, args.audio_only)

if __name__ == '__main__':
    main()