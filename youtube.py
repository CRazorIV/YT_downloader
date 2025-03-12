from pytubefix import YouTube
from tkinter import *
from tkinter import filedialog
import threading


def download_vid(save_path, url):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, file_extension='mp4')
        highest_resolution = streams.get_highest_resolution()
        highest_resolution.download(output_path=save_path)
        status_label.config(text="Video download complete!")
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
    status_label.config(text="Downloading...")

    # Run download in separate thread
    thread = threading.Thread(target=lambda: download_vid(save_path, url))
    thread.start()

    def check_thread():
        if thread.is_alive():
            root.after(100, check_thread)
        else:
            download_button.config(state=NORMAL)

    check_thread()


# Create main window
root = Tk()
root.title("YouTube MP4 Downloader")
root.geometry("800x400")

# URL Entry
Label(root, text="Enter YouTube URL:").pack(pady=10)
url_entry = Entry(root, width=50)
url_entry.pack(pady=5)

# Save Location
path_var = StringVar(value='C:/Users/yurik/Documents/GitHub/YT_downloader')
Label(root, text="Save Location:").pack(pady=5)
Entry(root, textvariable=path_var, width=50).pack(pady=5)
Button(root, text="Browse", command=browse_location).pack(pady=5)

# Download Button
download_button = Button(root, text="Download", command=start_download)
download_button.pack(pady=10)

# Status Label
status_label = Label(root, text="Ready to download")
status_label.pack(pady=10)

root.mainloop()