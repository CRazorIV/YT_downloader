from pytubefix import YouTube
from tkinter import *
from tkinter import ttk, filedialog
from ttkthemes import ThemedTk
import threading
def download_vid(save_path, url):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, file_extension='mp4')
        highest_resolution = streams.get_highest_resolution()

        # Get file size for progress bar
        file_size = highest_resolution.filesize
        progress['maximum'] = file_size

        def on_progress(stream, chunk, bytes_remaining):
            bytes_downloaded = file_size - bytes_remaining
            progress['value'] = bytes_downloaded
            percentage = (bytes_downloaded / file_size) * 100
            status_label.config(text=f"Downloading... {percentage:.1f}%")
            root.update_idletasks()

        yt.register_on_progress_callback(on_progress)
        highest_resolution.download(output_path=save_path)
        status_label.config(text="Video download complete!")
        progress['value'] = 0
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")


def browse_location():
    directory = filedialog.askdirectory()
    if directory:
        path_var.set(directory)


def start_download():
    url = url_entry.get()
    save_path = path_var.get()
    if not url:
        status_label.config(text="Please enter a URL")
        return

    download_button.config(state=DISABLED)
    progress['value'] = 0
    status_label.config(text="Initializing download...")

    thread = threading.Thread(target=lambda: download_vid(save_path, url))
    thread.start()

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

# Create style
style = ttk.Style()
style.configure("TEntry", padding=5)
style.configure("TButton", padding=5)
style.configure("Horizontal.TProgressbar", thickness=20)

# Main frame
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=BOTH, expand=True)

# URL Entry
ttk.Label(main_frame, text="Enter YouTube URL:", font=("Segoe UI", 10)).pack(pady=5)
url_entry = ttk.Entry(main_frame, width=50, font=("Segoe UI", 10))
url_entry.pack(pady=5)

# Save Location
path_var = StringVar(value='C:/Users/yurik/Documents/GitHub/YT_downloader')
ttk.Label(main_frame, text="Save Location:", font=("Segoe UI", 10)).pack(pady=5)
path_entry = ttk.Entry(main_frame, textvariable=path_var, width=50, font=("Segoe UI", 10))
path_entry.pack(pady=5)

# Browse Button
browse_button = ttk.Button(main_frame, text="Browse", command=browse_location)
browse_button.pack(pady=10)

# Download Button
download_button = ttk.Button(main_frame, text="Download", command=start_download)
download_button.pack(pady=10)

# Progress Bar
progress = ttk.Progressbar(main_frame, orient="horizontal", length=400, mode="determinate")
progress.pack(pady=10)

# Status Label
status_label = ttk.Label(main_frame, text="Ready to download", font=("Segoe UI", 10))
status_label.pack(pady=10)

root.mainloop()