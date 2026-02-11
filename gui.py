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
        self.root.geometry("700x600")
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
        input_frame = ttk.LabelFrame(main_frame, text="📌 Input", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Single URL
        ttk.Label(input_frame, text="Single Video URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        url_entry = ttk.Entry(input_frame, textvariable=self.url_var, width=60)
        url_entry.grid(row=0, column=1, columnspan=2, sticky=tk.EW, pady=5)
        
        # OR label
        ttk.Label(input_frame, text="— OR —", font=("Arial", 10, "bold")).grid(
            row=1, column=0, columnspan=3, pady=10
        )
        
        # Bulk file
        ttk.Label(input_frame, text="Bulk File (txt):").grid(row=2, column=0, sticky=tk.W, pady=5)
        file_entry = ttk.Entry(input_frame, textvariable=self.file_var, width=50, state="readonly")
        file_entry.grid(row=2, column=1, sticky=tk.EW, pady=5)
        
        browse_btn = ttk.Button(input_frame, text="Browse", command=self.browse_file)
        browse_btn.grid(row=2, column=2, padx=(5, 0), pady=5)
        
        input_frame.columnconfigure(1, weight=1)
        
        # Settings section
        settings_frame = ttk.LabelFrame(main_frame, text="⚙️ Settings", padding="10")
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
            text="📊 Get Video Size",
            command=self.get_video_size
        )
        get_size_btn.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        settings_frame.columnconfigure(1, weight=1)
        
        # Log section
        log_frame = ttk.LabelFrame(main_frame, text="📋 Download Log", padding="10")
        log_frame.pack(fill=tk.BOTH, pady=10)
        
        # Configure style for download button
        style = ttk.Style()
        style.configure('Big.TButton', font=('Arial', 12, 'bold'))
        
        self.download_btn = ttk.Button(
            button_frame,
            text="⬇️ START DOWNLOAD",
            command=self.start_download,
            style="Big.TButton",
            width=25
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Button section
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        self.download_btn = ttk.Button(
            button_frame,
            text="⬇️ Start Download",
            command=self.start_download,
            style="Accent.TButton"
        )
        self.download_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = ttk.Button(
            button_frame,
            text="🗑️ Clear Log",
            command=self.clear_log
        )
        clear_btn.pack(side=tk.LEFT)
        
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
                
            # Handle 2K/4K quality labels
            quality = self.quality_var.get()
            if "2K" in quality:
                quality = "1440p"
            elif "4K" in quality:
                quality = "2160p"
            
            downloader = YouTubeDownloader(
                output_dir=self.output_var.get(),
                quality=qualityrget_height and fmt.get('filesize'):
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
        self.log_text.delete(1.0, tk.END)
        
    def browse_file(self):
        """Browse for input file"""
        filename = filedialog.askopenfilename(
            title="Select URL list file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file_var.set(filename)
            self.url_var.set("")  # Clear URL if file is selected
            
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
            # Redirect stdout to log
            sys.stdout = TextRedirector(self.log_text, "stdout")
            
            downloader = YouTubeDownloader(
                output_dir=self.output_var.get(),
                quality=self.quality_var.get()
            )
            
            if url:
                downloader.download_single(url, self.audio_only_var.get())
            elif file:
                downloader.download_bulk(file, self.audio_only_var.get())
            
            self.status_var.set("Download completed!")
            messagebox.showinfo("Success", "Download completed successfully!")
            
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            self.status_var.set("Download failed!")
            messagebox.showerror("Error", f"Download failed:\n{str(e)}")
            
        finally:
            sys.stdout = sys.__stdout__
            self.is_downloading = False
            self.download_btn.config(state="normal")
            self.status_var.set("Ready")

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