from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from processor import process_csv

WATCH_DIR = "storage/app/medalists/"

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".csv"):
            print(f"New file detected: {event.src_path}")
            process_csv(event.src_path)

def watch_directory():
    observer = Observer()
    event_handler = FileHandler()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    observer.start()
    print(f"Watching directory: {WATCH_DIR}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    watch_directory()
