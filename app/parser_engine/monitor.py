'''
monitor the folder, if new .docx file is added:
docx examples from http://hhoppe.com/microsoft_word_examples.html
1.use mammoth convert .docx to .html
2.use pySBD to seg .html to sents
3.
'''
import time
import os
import mammoth
import pysbd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from database import write_to_db, write_to_html
from sentence_transformers import SentenceTransformer


PATH_TO_FAISS = "../models/faiss_index.pickle"
PATH_TO_PAPERS = "../models/papers.db"
DIRECTORY_TO_WATCH = "../static/docxs"
ST_MODEL = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
WIN_SIZE = 3
MAX_WORDS = 100


class Watcher:
    dir_to_watch = DIRECTORY_TO_WATCH

    def __init__(self):
        self.observer = Observer()

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

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)
            newfile = os.path.basename(event.src_path)
            if newfile.endswith(".docx"):
                write_to_db(event.src_path, PATH_TO_PAPERS, PATH_TO_FAISS, ST_MODEL, WIN_SIZE, MAX_WORDS)
                write_to_html(event.src_path)


if __name__ == '__main__':
    w = Watcher()
    w.run()
