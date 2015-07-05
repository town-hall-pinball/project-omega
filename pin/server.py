# Copyright (c) 2014 - 2015 townhallpinball.org
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import json
import logging
import os
from threading import Thread

import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket

import p

log = logging.getLogger("pin.server")
server = None
port = 9999

class Root(object):

    @cherrypy.expose
    def ws(self):
        # you can access the class instance through
        handler = cherrypy.request.ws_handler


class WebServer(Thread):

    def __init__(self):
        super(WebServer, self).__init__()
        cherrypy.config.update({
            "server.socket_host": "0.0.0.0",
            "server.socket_port": port,
            "log.screen": False,
            "engine.autoreload.on": False
        })


    def run(self):
        log.info("starting on port {}".format(port))
        plugin = WebSocketPlugin(cherrypy.engine)
        plugin.subscribe()
        cherrypy.tools.websocket = WebSocketTool()

        cherrypy.quickstart(Root(), "/", config={
            "/": {
                "tools.staticdir.on": True,
                "tools.staticdir.root": os.path.abspath(os.path.join(
                        os.path.dirname(__file__), "..", "web")),
                "tools.staticdir.index": "index.html",
                "tools.staticdir.dir": ""
            }
        })
        plugin.unsubscribe()
        log.info("stopped")


def update():
    if p.data["server_enabled"]:
        start()
    else:
        stop()

def start():
    global server
    if not server:
        server = WebServer()
        server.start()

def stop():
    global server
    if server:
        log.info("stopping")
        cherrypy.engine.exit()
        server = None


