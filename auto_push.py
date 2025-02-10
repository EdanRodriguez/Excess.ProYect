import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class GitAutoPushHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"File changed: {event.src_path}")
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Auto-update"], check=True)

            # Pull before pushing to avoid conflicts
            subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)


folder_to_track = r"C:\Users\edanr\OneDrive\Desktop\Code\Website\EdgeRunner"

event_handler = GitAutoPushHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()

try:
    print("Auto-push script running... Press Ctrl+C to stop.")
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopping auto-push...")
    observer.stop()
observer.join()
