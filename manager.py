import os
import time
import importlib
import multiprocessing
from src import bot

WATCH_PATH = '.'


def file_filter(name):
    return (
        not name.startswith(".") and
        not name.endswith(".pyc") and
        not name.endswith(".pyo") and
        not name.endswith("$py.class")
    )


def file_times():
    for top_level in filter(file_filter, os.listdir(WATCH_PATH)):
        for root, dirs, files in os.walk(top_level):
            for file in filter(file_filter, files):
                yield os.stat(os.path.join(root, file)).st_mtime


def watch_changes():
    last_mtime = max(file_times())
    while True:
        max_mtime = max(file_times())
        if max_mtime > last_mtime:
            last_mtime = max_mtime
            return
        time.sleep(1)


def run_autoreload():
    while True:
        importlib.reload(bot)
        p = multiprocessing.Process(target=bot.main, args=tuple())
        p.daemon = True
        p.start()
        watch_changes()
        p.terminate()
        print('Restarting the server.')
        while p.is_alive():
            time.sleep(1)


def main():
    try:
        run_autoreload()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
