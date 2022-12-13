class EnvEmptyValue(Exception):
    
    def __init__(self, message='Twitter entries are in the dovfile but values are missing'):
        self.message = message
        super().__init__(self.message)