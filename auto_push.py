import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class GitAutoPushHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"File changed: {event.src_path}")
            subprocess.run(["git", "add", "."], check=True)

            # Check if there are changes before committing
            status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
            if status.stdout.strip():  # If there are changes
                subprocess.run(["git", "commit", "-m", "Auto-update"], check=True)

                # Pull before pushing to avoid conflicts
                try:
                    subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=True)
                except subprocess.CalledProcessError:
                    print("Rebase conflict detected. Resolve manually.")
                    return
                
                subprocess.run(["git", "push", "origin", "main"], check=True)
            else:
                print("No changes to commit.")


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
