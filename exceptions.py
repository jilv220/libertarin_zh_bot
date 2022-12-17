class EnvEmptyValue(Exception):

    def __init__(self, message='Entries are in the dovenv file but values may be missing'):
        self.message = message
        super().__init__(self.message)

class UnknownTranslator(Exception):
    def __init__(self, message='Translator not supported yet'):
        self.message = message
        super().__init__(self.message)