import logging

class Logger:

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s [%(name)s] [%(levelname)s] %(message)s'
        )
        ch.setFormatter(formatter)
        ch.setLevel(logging.DEBUG)

        self.logger.addHandler(ch)
        self.logger.propagate = False

    def error(self, msg):
        self.logger.error(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def info(self, msg):
        self.logger.info(msg)