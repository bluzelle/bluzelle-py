from bluzelle import bzapi
import logging

class DefaultLogging(bzapi.logger):

    def __init__(self):
        bzapi.logger.__init__(self)

        # Configure Python logging module root logger
        # logging.basicConfig(format='%(asctime)s  %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
        #                     level=logging.INFO)

    def log(self, severity, message):
        #logging.log(severity, message)
        print(severity, message)