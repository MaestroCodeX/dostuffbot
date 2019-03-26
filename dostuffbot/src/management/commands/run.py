import os
import time
import types
import importlib
import multiprocessing

from django.core.management.base import BaseCommand

import env

WATCH_PATH = '.'


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            self.run_autoreload()
        except KeyboardInterrupt:
            pass

    def file_filter(self, name):
        return (
            not name.startswith(".") and
            not name.endswith(".pyc") and
            not name.endswith(".pyo") and
            not name.endswith("$py.class")
        )

    def file_times(self):
        for top_level in filter(self.file_filter, os.listdir(WATCH_PATH)):
            for root, dirs, files in os.walk(top_level):
                for file in filter(self.file_filter, files):
                    yield os.stat(os.path.join(root, file)).st_mtime

    def watch_changes(self):
        last_mtime = max(self.file_times())
        while True:
            max_mtime = max(self.file_times())
            if max_mtime > last_mtime:
                last_mtime = max_mtime
                return
            time.sleep(1)

    def imports(self, module):
        for name, val in vars(module).items():
            if isinstance(val, types.ModuleType):
                yield val.__name__

    def reload_module(self, module):
        importlib.reload(module)
        for m_str in self.imports(module):
            m = importlib.import_module(m_str)
            importlib.reload(m)

    def run_autoreload(self):
        module = importlib.import_module(env.MODULE_PATH)
        while True:
            p = multiprocessing.Process(target=module.main, args=tuple())
            p.daemon = True
            p.start()
            self.watch_changes()
            p.terminate()
            print('Restarting the server.')
            while p.is_alive():
                time.sleep(1)
            self.reload_module(module)
