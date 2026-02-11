# 📥 YouTube Video Downloader

A powerful, easy-to-use YouTube video downloader with GUI support. Download single videos or bulk downloads from text files up to 1080p quality.

## ✨ Features

- 🎬 Download YouTube videos up to 1080p
- 📋 Bulk download from text file (multiple URLs)
- 🎵 Extract audio only (MP3)
- 🖥️ Simple GUI interface
- ⚡ Fast downloads with resume support
- 📊 Progress tracking
- 🔄 Automatic retry on failure
- 🎯 Quality selection (360p, 480p, 720p, 1080p)

## 🚀 Quick Start

### Windows Users

1. **Download and run the installer:**
   ```bash
   # Clone this repository
   git clone https://github.com/raowaqar000/Youtube-Video-Downloader.git
   cd Youtube-Video-Downloader
   
   # Run the installer
   install.bat
   ```

2. **Launch the downloader:**
   ```bash
   start_downloader.bat
   ```

### Linux/Mac Users

```bash
# Clone repository
git clone https://github.com/raowaqar000/Youtube-Video-Downloader.git
cd Youtube-Video-Downloader

# Make scripts executable
chmod +x install.sh start_downloader.sh

# Install dependencies
./install.sh

# Launch downloader
./start_downloader.sh
```

## 📖 Usage

### Method 1: GUI Interface (Easiest)

1. Run `start_downloader.bat` (Windows) or `./start_downloader.sh` (Linux/Mac)
2. Enter YouTube URL or browse for a text file with multiple URLs
3. Select quality (360p, 480p, 720p, 1080p, or Audio Only)
4. Choose download location
5. Click "Download"

### Method 2: Command Line

```bash
# Single video download (best quality up to 1080p)
python downloader.py --url "https://www.youtube.com/watch?v=VIDEO_ID"

# Bulk download from text file
python downloader.py --file urls.txt

# Download audio only
python downloader.py --url "VIDEO_URL" --audio-only

# Specify quality
python downloader.py --url "VIDEO_URL" --quality 720p

# Specify output folder
python downloader.py --file urls.txt --output ./downloads
```

## 📝 Text File Format

Create a text file with one URL per line:

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://www.youtube.com/watch?v=9bZkp7q19f0
https://www.youtube.com/watch?v=kJQP7kiw5Fk
```

## 🛠️ Requirements

- Python 3.7 or higher
- Internet connection
- ~100MB free disk space for dependencies

## 📦 Dependencies

All dependencies are automatically installed by the installer script:
- `yt-dlp` - YouTube download engine
- `tkinter` - GUI interface (included with Python)
- `ffmpeg` - Video/audio processing

## 🎯 Supported Qualities

- 🎬 **1080p** (Full HD)
- 🎬 **720p** (HD)
- ���� **480p** (SD)
- 🎬 **360p** (Mobile)
- 🎵 **Audio Only** (MP3, 320kbps)

## 📁 Project Structure

```
Youtube-Video-Downloader/
├── downloader.py          # Main downloader script
├── gui.py                 # GUI interface
├── install.bat            # Windows installer
├── install.sh             # Linux/Mac installer
├── start_downloader.bat   # Windows launcher
├── start_downloader.sh    # Linux/Mac launcher
├── requirements.txt       # Python dependencies
├── config.json           # Configuration file
└── README.md             # This file
```

## ⚙️ Configuration

Edit `config.json` to customize default settings:

```json
{
    "default_quality": "1080p",
    "download_folder": "./downloads",
    "max_retries": 3,
    "audio_format": "mp3",
    "audio_quality": "320"
}
```

## 🐛 Troubleshooting

**Problem: "yt-dlp not found"**
- Solution: Run the installer script again

**Problem: "FFmpeg not found"**
- Solution: The installer will download it automatically

**Problem: Video won't download**
- Solution: Check if the URL is correct and the video is not private/age-restricted

**Problem: Low quality only**
- Solution: Some videos don't have 1080p. Try 720p instead

## 📜 License

MIT License - Feel free to use and modify

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## ⚠️ Disclaimer

This tool is for personal use only. Respect copyright laws and YouTube's Terms of Service. Don't redistribute downloaded content without permission.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

Made with ❤️ by raowaqar000