import os
import time
import types
import importlib
import multiprocessing
import env

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


def imports(module):
    for name, val in vars(module).items():
        if isinstance(val, types.ModuleType):
            yield val.__name__


def reload_module(module):
    importlib.reload(module)
    for m_str in imports(module):
        m = importlib.import_module(m_str)
        importlib.reload(m)


def run_autoreload():
    module = importlib.import_module(env.MODULE_PATH)
    while True:
        p = multiprocessing.Process(target=module.main, args=tuple())
        p.daemon = True
        p.start()
        watch_changes()
        p.terminate()
        print('Restarting the server.')
        while p.is_alive():
            time.sleep(1)
        reload_module(module)


def main():
    try:
        run_autoreload()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
