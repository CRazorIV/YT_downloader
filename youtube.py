from pytubefix import YouTube
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk
import threading
import os


def download_vid(save_path, url):
    try:
        # Validate URL before proceeding
        if not url.startswith(('https://www.youtube.com', 'https://youtu.be')):
            root.after(0, lambda: status_label.config(text="Error: Invalid YouTube URL"))
            return

        # Create directory if it doesn't exist
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        yt = YouTube(url)

        # Set up progress callback before creating streams
        def on_progress(stream, chunk, bytes_remaining):
            if stream.filesize:  # Ensure filesize is available
                bytes_downloaded = stream.filesize - bytes_remaining
                # Update UI safely using after method
                root.after(0, lambda: update_progress(bytes_downloaded, stream.filesize))

        yt.register_on_progress_callback(on_progress)

        # Get streams after registering callback
        streams = yt.streams.filter(progressive=True, file_extension='mp4')
        if not streams:
            root.after(0, lambda: status_label.config(text="Error: No suitable streams found"))
            return

        highest_resolution = streams.get_highest_resolution()

        # Download the video
        highest_resolution.download(output_path=save_path)

        # Update UI after download completes
        root.after(0, lambda: status_label.config(text=f"Download complete: {yt.title}"))
        root.after(0, lambda: progress.config(value=0))

    except Exception as e:
        # Update UI with error message
        root.after(0, lambda: status_label.config(text=f"Error: {str(e)}"))


def update_progress(bytes_downloaded, file_size):
    """Update progress bar and status label safely from any thread"""
    progress['maximum'] = file_size
    progress['value'] = bytes_downloaded
    percentage = (bytes_downloaded / file_size) * 100
    status_label.config(text=f"Downloading... {percentage:.1f}%")
    # Force update the UI
    root.update_idletasks()


def browse_location():
    directory = filedialog.askdirectory()
    if directory:
        path_var.set(directory)


def start_download():
    url = url_entry.get().strip()
    save_path = path_var.get()

    if not url:
        status_label.config(text="Please enter a URL")
        return

    if not save_path:
        status_label.config(text="Please select a save location")
        return

    # Disable download button and reset progress
    download_button.config(state=DISABLED)
    progress['value'] = 0
    status_label.config(text="Initializing download...")

    # Start download in a separate thread
    thread = threading.Thread(target=lambda: download_vid(save_path, url))
    thread.daemon = True  # Thread will close when main program exits
    thread.start()

    # Check thread status periodically
    def check_thread():
        if thread.is_alive():
            root.after(100, check_thread)
        else:
            download_button.config(state=NORMAL)

    check_thread()


# Create themed window
root = ThemedTk(theme="yaru")
root.title("YouTube MP4 Downloader")
root.geometry("600x400")
root.minsize(500, 350)  # Set minimum window size

# Set color scheme
bg_color = "#2E3440"
fg_color = "#ECEFF4"
btn_fg_color = "#000000"
accent_color = "#5E81AC"
button_color = "#81A1C1"
entry_bg = "#3B4252"

# Configure the root window
root.configure(bg=bg_color)

# Create style with colors
style = ttk.Style()
style.configure("TFrame", background=bg_color)
style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Segoe UI", 10))
style.configure("TEntry", padding=5, fieldbackground=entry_bg, foreground=fg_color)
style.configure("TButton", padding=5, background=button_color, foreground=btn_fg_color)
style.configure("Horizontal.TProgressbar", background=accent_color, troughcolor=entry_bg, thickness=20)

# Main frame
main_frame = ttk.Frame(root, padding="20", style="TFrame")
main_frame.pack(fill=BOTH, expand=True)

# Configure grid for better resizing
main_frame.columnconfigure(0, weight=1)
for i in range(10):  # Adjust based on number of rows
    main_frame.rowconfigure(i, weight=0)

# URL Entry
url_label = ttk.Label(main_frame, text="Enter YouTube URL:", style="TLabel")
url_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

url_entry = ttk.Entry(main_frame, font=("Segoe UI", 10), foreground="black", background=entry_bg)
url_entry.grid(row=1, column=0, sticky="ew", pady=(0, 10))

# Save Location
path_label = ttk.Label(main_frame, text="Save Location:", style="TLabel")
path_label.grid(row=2, column=0, sticky="w", pady=(0, 5))

path_var = StringVar(value='path/to/download/folder')
path_entry = ttk.Entry(main_frame, textvariable=path_var, font=("Segoe UI", 10), foreground="black", background=entry_bg)
path_entry.grid(row=3, column=0, sticky="ew", pady=(0, 10))

# Button frame for better layout
button_frame = ttk.Frame(main_frame, style="TFrame")
button_frame.grid(row=4, column=0, sticky="ew", pady=10)
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)

# Browse Button
browse_button = ttk.Button(button_frame, text="Browse", command=browse_location)
browse_button.grid(row=0, column=0, padx=(0, 5), sticky="e")

# Download Button
download_button = ttk.Button(button_frame, text="Download", command=start_download)
download_button.grid(row=0, column=1, padx=(5, 0), sticky="w")

# Progress Bar
progress = ttk.Progressbar(main_frame, orient="horizontal", mode="determinate")
progress.grid(row=5, column=0, sticky="ew", pady=15)

# Status Label
status_label = ttk.Label(main_frame, text="Ready to download", style="TLabel")
status_label.grid(row=6, column=0, sticky="w", pady=10)


# Add a function to delay resize updates
def delayed_resize(event=None):
    if hasattr(root, '_resize_job'):
        root.after_cancel(root._resize_job)
    root._resize_job = root.after(100, lambda: None)  # Just wait, no action needed


# Bind the resize event
root.bind("<Configure>", delayed_resize)

root.mainloop()