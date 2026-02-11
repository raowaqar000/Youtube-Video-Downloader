#!/usr/bin/env python3
"""
YouTube Video Downloader - GUI Interface
Simple and user-friendly graphical interface
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from pathlib import Path
import threading
import sys
import os

# Import downloader
from downloader import YouTubeDownloader

class DownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("700x650")
        self.root.resizable(False, False)
        
        # Variables
        self.url_var = tk.StringVar()
        self.file_var = tk.StringVar()
        self.quality_var = tk.StringVar(value="1080p")
        self.audio_only_var = tk.BooleanVar(value=False)
        self.output_var = tk.StringVar(value="./downloads")
        self.video_size_var = tk.StringVar(value="Size: N/A")
        self.is_downloading = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            title_frame, 
            text="📥 YouTube Video Downloader",
            font=("Arial", 18, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Download YouTube videos up to 4K quality with size preview",
            font=("Arial", 10)
        )
        subtitle_label.pack()
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Single URL
        ttk.Label(input_frame, text="Single Video URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        url_entry = ttk.Entry(input_frame, textvariable=self.url_var, width=60)
        url_entry.grid(row=0, column=1, columnspan=3, sticky=tk.EW, pady=5)
        
        # OR label
        ttk.Label(input_frame, text="— OR —", font=("Arial", 10, "bold")).grid(
            row=1, column=0, columnspan=4, pady=10
        )
        
        # Bulk file
        ttk.Label(input_frame, text="Bulk File (txt):").grid(row=2, column=0, sticky=tk.W, pady=5)
        file_entry = ttk.Entry(input_frame, textvariable=self.file_var, width=50)
        file_entry.grid(row=2, column=1, sticky=tk.EW, pady=5)
        
        browse_btn = ttk.Button(input_frame, text="Browse", command=self.browse_file)
        browse_btn.grid(row=2, column=2, padx=(5, 0), pady=5)
        
        clear_file_btn = ttk.Button(input_frame, text="Clear", command=self.clear_file)
        clear_file_btn.grid(row=2, column=3, padx=(5, 0), pady=5)
        
        # Download buttons inside input frame
        button_inner_frame = ttk.Frame(input_frame)
        button_inner_frame.grid(row=3, column=0, columnspan=4, pady=(15, 5), sticky=tk.EW)
        
        # Configure style for download button
        style = ttk.Style()
        style.configure('Big.TButton', font=('Arial', 11, 'bold'))
        
        self.download_btn = ttk.Button(
            button_inner_frame,
            text="START DOWNLOAD",
            command=self.start_download,
            style="Big.TButton"
        )
        self.download_btn.pack(side=tk.LEFT, padx=(0, 10), ipadx=15, ipady=5)
        
        stop_btn = ttk.Button(
            button_inner_frame,
            text="Stop",
            command=self.stop_download
        )
        stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_log_btn = ttk.Button(
            button_inner_frame,
            text="Clear Log",
            command=self.clear_log
        )
        clear_log_btn.pack(side=tk.LEFT)
        
        input_frame.columnconfigure(1, weight=1)
        
        # Settings section
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Quality selection
        ttk.Label(settings_frame, text="Quality:").grid(row=0, column=0, sticky=tk.W, pady=5)
        quality_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.quality_var,
            values=["360p", "480p", "720p", "1080p", "1440p (2K)", "2160p (4K)"],
            state="readonly",
            width=15
        )
        quality_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Audio only checkbox
        audio_check = ttk.Checkbutton(
            settings_frame,
            text="Audio Only (MP3)",
            variable=self.audio_only_var
        )
        audio_check.grid(row=0, column=2, padx=20, pady=5)
        
        # Output folder
        ttk.Label(settings_frame, text="Output Folder:").grid(row=1, column=0, sticky=tk.W, pady=5)
        output_entry = ttk.Entry(settings_frame, textvariable=self.output_var, width=40)
        output_entry.grid(row=1, column=1, columnspan=2, sticky=tk.EW, pady=5)
        
        browse_output_btn = ttk.Button(
            settings_frame,
            text="Browse",
            command=self.browse_output
        )
        browse_output_btn.grid(row=1, column=3, padx=(5, 0), pady=5)
        
        # Video size info
        size_label = ttk.Label(settings_frame, textvariable=self.video_size_var, foreground="blue")
        size_label.grid(row=2, column=0, columnspan=4, sticky=tk.W, pady=5)
        
        # Get size button
        get_size_btn = ttk.Button(
            settings_frame,
            text="Get Video Size",
            command=self.get_video_size
        )
        get_size_btn.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        settings_frame.columnconfigure(1, weight=1)
        
        # Log section
        log_frame = ttk.LabelFrame(main_frame, text="Download Log", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create log_text widget
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding="5"
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def log(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def clear_log(self):
        """Clear the log"""
        self.log_text.delete(1.0, tk.END)
    
    def clear_file(self):
        """Clear the selected file"""
        self.file_var.set("")
    
    def stop_download(self):
        """Stop the current download"""
        if self.is_downloading:
            self.is_downloading = False
            self.status_var.set("Stopping...")
            self.log("⚠️ Stop requested - will stop after current download")
    
    def get_video_size(self):
        """Get video size information"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("No URL", "Please enter a video URL first!")
            return
        
        self.video_size_var.set("Fetching size...")
        self.root.update()
        
        thread = threading.Thread(target=self.fetch_video_size, args=(url,))
        thread.daemon = True
        thread.start()
    
    def fetch_video_size(self, url):
        """Fetch video size in a separate thread"""
        try:
            import subprocess
            import json
            
            # Get quality (handle 2K/4K labels)
            quality = self.quality_var.get()
            if "2K" in quality:
                quality = "1440p"
            elif "4K" in quality:
                quality = "2160p"
            
            # Get video info using yt-dlp
            cmd = ['yt-dlp', '--dump-json', '--no-warnings', url]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                info = json.loads(result.stdout)
                title = info.get('title', 'Unknown')
                duration = info.get('duration', 0)
                
                # Find the best format matching quality
                formats = info.get('formats', [])
                target_height = int(quality.replace('p', ''))
                
                best_format = None
                for fmt in formats:
                    if fmt.get('height') == target_height and fmt.get('filesize'):
                        best_format = fmt
                        break
                
                if not best_format:
                    # Try to find closest format with size
                    for fmt in sorted(formats, key=lambda x: abs((x.get('height', 0) or 0) - target_height)):
                        if fmt.get('filesize'):
                            best_format = fmt
                            break
                
                if best_format and best_format.get('filesize'):
                    filesize = best_format['filesize']
                    size_mb = filesize / (1024 * 1024)
                    size_gb = size_mb / 1024
                    
                    if size_gb >= 1:
                        size_str = f"{size_gb:.2f} GB"
                    else:
                        size_str = f"{size_mb:.2f} MB"
                    
                    duration_str = f"{int(duration // 60)}:{int(duration % 60):02d}"
                    self.video_size_var.set(f"📊 Size: {size_str} | Duration: {duration_str} | Title: {title[:50]}...")
                else:
                    self.video_size_var.set(f"📊 Size: Unavailable | Duration: {int(duration // 60)}:{int(duration % 60):02d}")
            else:
                self.video_size_var.set("❌ Failed to fetch video info")
                
        except subprocess.TimeoutExpired:
            self.video_size_var.set("❌ Timeout - Try again")
        except Exception as e:
            self.video_size_var.set(f"❌ Error: {str(e)}")
        
    def browse_file(self):
        """Browse for input file"""
        filename = filedialog.askopenfilename(
            title="Select URL list file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file_var.set(filename)
            self.url_var.set("")  # Clear URL if file is selected
            # Show how many URLs are in the file
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    urls = [line.strip() for line in f if line.strip() and line.strip().startswith('http')]
                self.log(f"📋 Loaded {len(urls)} URLs from file")
            except Exception as e:
                self.log(f"❌ Error reading file: {e}")
            
    def browse_output(self):
        """Browse for output folder"""
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_var.set(folder)
            
    def start_download(self):
        """Start the download process"""
        if self.is_downloading:
            messagebox.showwarning("Download in Progress", "A download is already in progress!")
            return
        
        url = self.url_var.get().strip()
        file = self.file_var.get().strip()
        
        if not url and not file:
            messagebox.showerror("No Input", "Please enter a URL or select a file!")
            return
        
        # Start download in separate thread
        self.is_downloading = True
        self.download_btn.config(state="disabled")
        self.status_var.set("Downloading...")
        
        thread = threading.Thread(target=self.download_thread, args=(url, file))
        thread.daemon = True
        thread.start()
        
    def download_thread(self, url, file):
        """Download thread"""
        try:
            # Handle 2K/4K quality labels
            quality = self.quality_var.get()
            if "2K" in quality:
                quality = "1440p"
            elif "4K" in quality:
                quality = "2160p"
            
            downloader = YouTubeDownloader(
                output_dir=self.output_var.get(),
                quality=quality
            )
            
            if url:
                self.log(f"🎬 Starting download: {url}")
                self.log(f"📊 Quality: {quality}")
                self.download_with_logging(downloader, url, self.audio_only_var.get())
            elif file:
                self.log(f"📋 Starting bulk download from: {file}")
                self.log(f"📊 Quality: {quality}")
                self.bulk_download_with_logging(downloader, file, self.audio_only_var.get())
            
            if self.is_downloading:
                self.status_var.set("Download completed!")
                self.root.after(0, lambda: messagebox.showinfo("Success", "Download completed successfully!"))
            else:
                self.status_var.set("Download stopped")
            
        except Exception as e:
            err_msg = str(e)
            self.log(f"❌ Error: {err_msg}")
            self.status_var.set("Download failed!")
            self.root.after(0, lambda msg=err_msg: messagebox.showerror("Error", f"Download failed:\n{msg}"))
            
        finally:
            self.is_downloading = False
            self.root.after(0, lambda: self.download_btn.config(state="normal"))
            self.root.after(0, lambda: self.status_var.set("Ready"))
    
    def download_with_logging(self, downloader, url, audio_only):
        """Download single video with GUI logging"""
        import subprocess
        
        format_string = downloader.get_format_string(downloader.quality, audio_only)
        
        cmd = [
            'yt-dlp',
            '-f', format_string,
            '-o', str(downloader.output_dir / '%(title)s.%(ext)s'),
            '--no-overwrites',
            '--continue',
            '--ignore-errors',
            '--newline',
            '--progress',
        ]
        
        if audio_only:
            cmd.extend([
                '-x',
                '--audio-format', downloader.audio_format,
                '--audio-quality', downloader.audio_quality,
            ])
        else:
            cmd.extend([
                '--merge-output-format', 'mp4',
            ])
        
        cmd.append(url)
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            for line in process.stdout:
                if not self.is_downloading:
                    process.terminate()
                    break
                line = line.strip()
                if line:
                    self.root.after(0, lambda l=line: self.log(l))
            
            process.wait()
            
            if process.returncode == 0:
                self.root.after(0, lambda: self.log("✅ Download completed!"))
                return True
            else:
                self.root.after(0, lambda: self.log("❌ Download failed"))
                return False
                
        except Exception as e:
            err_msg = str(e)
            self.root.after(0, lambda msg=err_msg: self.log(f"❌ Error: {msg}"))
            return False
    
    def bulk_download_with_logging(self, downloader, file_path, audio_only):
        """Download multiple videos with GUI logging"""
        from pathlib import Path
        
        file_path = Path(file_path)
        
        if not file_path.exists():
            self.root.after(0, lambda: self.log(f"❌ File not found: {file_path}"))
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and line.strip().startswith('http')]
        
        if not urls:
            self.root.after(0, lambda: self.log("❌ No valid URLs found in file"))
            return
        
        self.root.after(0, lambda: self.log(f"\n📋 Found {len(urls)} URLs to download"))
        
        success_count = 0
        failed_urls = []
        
        for i, url in enumerate(urls, 1):
            if not self.is_downloading:
                self.root.after(0, lambda: self.log("\n⚠️ Download stopped by user"))
                break
                
            self.root.after(0, lambda i=i, total=len(urls): self.log(f"\n{'='*50}"))
            self.root.after(0, lambda i=i, total=len(urls): self.log(f"📥 Downloading {i}/{total}"))
            self.root.after(0, lambda u=url: self.log(f"URL: {u}"))
            self.root.after(0, lambda: self.status_var.set(f"Downloading {i}/{len(urls)}..."))
            
            if self.download_with_logging(downloader, url, audio_only):
                success_count += 1
            else:
                failed_urls.append(url)
        
        # Summary
        self.root.after(0, lambda: self.log(f"\n{'='*50}"))
        self.root.after(0, lambda: self.log(f"📊 DOWNLOAD SUMMARY"))
        self.root.after(0, lambda: self.log(f"{'='*50}"))
        self.root.after(0, lambda s=success_count, t=len(urls): self.log(f"✅ Successful: {s}/{t}"))
        self.root.after(0, lambda f=len(failed_urls), t=len(urls): self.log(f"❌ Failed: {f}/{t}"))
        
        if failed_urls:
            self.root.after(0, lambda: self.log(f"\n❌ Failed URLs:"))
            for url in failed_urls:
                self.root.after(0, lambda u=url: self.log(f"  - {u}"))

class TextRedirector:
    """Redirect text output to tkinter widget"""
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)

    def flush(self):
        pass

def main():
    root = tk.Tk()
    app = DownloaderGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()