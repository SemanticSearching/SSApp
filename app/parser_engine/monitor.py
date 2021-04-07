'''
monitor the folder, if new .docx file is added:
docx examples from http://hhoppe.com/microsoft_word_examples.html
1.use mammoth convert .docx to .html
2.use pySBD to seg .html to sents
3.
'''
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from database import write_to_db, write_to_html
from app.config import Config as cf


class Watcher:

    def __init__(self, dir_to_watch):
        self.observer = Observer()
        self.dir_to_watch = dir_to_watch

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.dir_to_watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")
        self.observer.join()


class Handler(FileSystemEventHandler):

    def __init__(self, path_to_papers, path_to_faiss, st_model, win_size, max_words, host, handler_obj):
        self.path_to_papers = path_to_papers
        self.path_to_faiss = path_to_faiss
        self.st_model = st_model
        self.win_size = win_size
        self.max_words = max_words
        self.host = host

    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)
            newfile = os.path.basename(event.src_path)
            if newfile.endswith(".docx"):
                write_to_db(event.src_path, self.path_to_papers, self.path_to_faiss, self.st_model, self.win_size, self.max_words, self.host)
                write_to_html(event.src_path)


class ReloadHandler(FileSystemEventHandler):

    def __init__(self, path_to_papers, path_to_faiss, st_model, win_size, max_words, host):
        self.path_to_papers = path_to_papers
        self.path_to_faiss = path_to_faiss
        self.st_model = st_model
        self.win_size = win_size
        self.max_words = max_words
        self.host = host

    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)
            newfile = os.path.basename(event.src_path)
            if newfile.endswith(".docx"):
                write_to_db(event.src_path, self.path_to_papers, self.path_to_faiss, self.st_model, self.win_size, self.max_words, self.host)
                write_to_html(event.src_path)


if __name__ == '__main__':
    w = Watcher()
    w.run()
