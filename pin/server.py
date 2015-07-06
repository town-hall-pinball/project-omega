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
from pin import brand

log = logging.getLogger("pin.server")
log_command = logging.getLogger("pin.command")
server = None
port = 9999

class Root(object):

    @cherrypy.expose
    def ws(self):
        handler = cherrypy.request.ws_handler

    def get_branding(self):
        return {
            "name": brand.name,
            "version": brand.version,
            "release": brand.release
        }

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def branding(self):
        return self.get_branding()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def status(self):
        devices = {}
        def add_devices(ds):
            for d in ds.values():
                devices[d.device] = d.__dict__
        add_devices(p.coils)
        add_devices(p.flashers)
        add_devices(p.gi)
        add_devices(p.lamps)
        add_devices(p.switches)

        return {
            "branding": self.get_branding(),
            "devices": devices
        }


class Handler(WebSocket):

    def received_message(self, m):
        if not p.data["server_remote_control"]:
            return
        message = json.loads(str(m))
        command = message["command"]
        log_command.debug(command)
        if command == "switch":
            self.toggle_switch(message)

    def toggle_switch(self, message):
        switch = p.switches[message["name"]]
        change_to = not switch.active
        if change_to:
            event = p.proc.SWITCH_OPENED if switch.opto else p.proc.SWITCH_CLOSED
        else:
            event = p.proc.SWITCH_CLOSED if switch.opto else p.proc.SWITCH_OPENED
        p.proc.artificial_events += [{"type": event, "value": switch.number}]


class WebServer(Thread):

    def __init__(self):
        super(WebServer, self).__init__()
        cherrypy.config.update({
            "server.socket_host": "0.0.0.0",
            "server.socket_port": port,
            "log.screen": False,
            "engine.autoreload.on": False
        })

    def dispatch_device(self, item, *args, **kwargs):
        if not p.data["server_publish_events"]:
            return
        payload = item.__dict__
        payload["message"] = item.type
        cherrypy.engine.publish("websocket-broadcast", json.dumps(payload))

    def run(self):
        log.info("starting on port {}".format(port))
        plugin = WebSocketPlugin(cherrypy.engine)
        plugin.subscribe()
        cherrypy.tools.websocket = WebSocketTool()

        p.events.on("switch", self.dispatch_device)

        cherrypy.quickstart(Root(), "/", config={
            "/": {
                "tools.staticdir.on": True,
                "tools.staticdir.root": os.path.abspath(os.path.join(
                        os.path.dirname(__file__), "..", "web")),
                "tools.staticdir.index": "index.html",
                "tools.staticdir.dir": ""
            },
            "/console": {
                "tools.staticdir.on": True,
                "tools.staticdir.dir": "console"
            },
            "/ws": {
                "tools.websocket.on": True,
                "tools.websocket.handler_cls": Handler
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


