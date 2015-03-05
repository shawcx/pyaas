
import pyaas.web

class ExampleApp(pyaas.web.Application):
    def __init__(self):
        # important to use extend if using built-in authentication
        self.patterns = [
            ( r'/',       pyaas.web.handlers.Index     ),
            ( r'/(main)', pyaas.web.handlers.Protected ),
            ]

        pyaas.web.Application.__init__(self)
