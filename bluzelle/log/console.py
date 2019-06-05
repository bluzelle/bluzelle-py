from bluzelle import bzapi

class ConsoleLogger(bzapi.logger):

    def __init__(self):
        bzapi.logger.__init__(self)
    def log(self, severity, message):
        print(severity, message)