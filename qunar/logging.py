from . import settings


class Logger:
    """日志工具"""

    def __init__(self, prefix='Unknown'):
        self._debug = settings.DEBUG
        self.prefix = prefix

    def info(self, msg):
        print(f'[INFO][{self.prefix}]{msg}')

    def debug(self, msg):
        if self._debug:
            print(f'[DEBUG][{self.prefix}]{msg}')
