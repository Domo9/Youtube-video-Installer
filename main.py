from pytube import YouTube
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def download_video(url, status_label, progress_bar):
    if not url.strip():
        messagebox.showwarning("Input Error", "Please enter a valid YouTube URL!")
        return

    try:
        folder = filedialog.askdirectory()
        if not folder:
            messagebox.showwarning("No Folder", "No folder selected!")
            return

        yt = YouTube(url, on_progress_callback=lambda stream, chunk, bytes_remaining: update_progress(stream, bytes_remaining, progress_bar))
        stream = yt.streams.filter(progressive=True, file_extension="mp4").get_highest_resolution()

        status_label.config(text="Downloading...")
        progress_bar["value"] = 0
        root.update_idletasks()

        stream.download(output_path=folder)

        status_label.config(text=f"Downloaded to: {folder}")
        messagebox.showinfo("Success", f"Video downloaded to:\n{folder}")

    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")
        status_label.config(text="Download failed.")

def update_progress(stream, bytes_remaining, progress_bar):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    progress_bar["value"] = percentage
    root.update_idletasks()

def gui():
    global root
    root = tk.Tk()
    root.title("YouTube Downloader")
    root.geometry("450x250")

    label = tk.Label(root, text="Enter YouTube URL:")
    label.pack(pady=5)

    entry = tk.Entry(root, width=50)
    entry.pack(pady=5)

    status_label = tk.Label(root, text="", fg="blue")
    status_label.pack(pady=5)

    progress_bar = ttk.Progressbar(root, length=300, mode="determinate")
    progress_bar.pack(pady=5)

    button = tk.Button(root, text="Download", command=lambda: download_video(entry.get(), status_label, progress_bar))
    button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    gui()
