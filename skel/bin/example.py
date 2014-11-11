#!/usr/bin/env python

# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# -----------------------------------------------------------------------------

# The above license applies only to the example project. The intent is to allow
# you to freely use this template for your project and license it as you see
# fit. The pyaas library is released under the MIT License.

# -----------------------------------------------------------------------------

# This file can live in the base directory of the project or in a ./bin
# directory and init() (see below) will resolve accordingly

# This bit just ensures that this file isn't on the module search path
import inspect, os, sys
localpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path = filter(lambda path: path != localpath, sys.path)

import logging

import pyaas
import example
import example.app

def runExampleApp():
    # Set the root for pyaas to this directory
    # If a path is not passed then pyaas will derive the path
    #
    # Set the namespace for the project,
    # e.g. etc/example.ini vs etc/example/example.ini
    # -or- share/static/favicon.ico vs share/example/static/favicon.ico
    #
    # Calling init() without args is equivalent to:
    # pyaas.init(prefix='/full/path/to/example', namespace='example', settings='example')

    pyaas.init()

    app = example.app.ExampleApp()
    try:
        app.Listen()
    except KeyboardInterrupt:
        app.Stop()

if '__main__' == __name__:
    try:
        runExampleApp()
    except pyaas.error as e:
        logging.exception('%s', e)
