
import pyaas
import pyaas.handlers

class ExampleApp(pyaas.server.Application):
    def __init__(self):
        # important to use extend if using built-in authentication
        self.patterns = [
            ( r'/',       pyaas.handlers.Index     ),
            ( r'/(main)', pyaas.handlers.Protected ),
            ]

        pyaas.server.Application.__init__(self)