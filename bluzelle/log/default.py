from bluzelle import bzapi
import logging
import sys

class DefaultLogger(bzapi.logger):

    def __init__(self):
        bzapi.logger.__init__(self)
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def log(self, severity, message):
        getattr(logging, severity)(message)