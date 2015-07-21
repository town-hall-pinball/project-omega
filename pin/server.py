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
from pin import ball, brand, keyboard
from pin.handler import Handler

log = logging.getLogger("pin.server")
log_command = logging.getLogger("pin.command")
server = None
port = 9999

class Root(object):

    @cherrypy.expose
    def ws(self):
        pass

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

        keymap = []
        for key, action in keyboard.keys.items():
            mods = ""
            if len(key) > 1:
                mods = key[:-1]
                key = key[-1]
            keymap += [{"key": key, "mods": mods, "action": action["name"]}]

        return {
            "branding": self.get_branding(),
            "devices": devices,
            "keymap": keymap,
        }


class WebSocketHandler(WebSocket):

    def received_message(self, m):
        if not p.data["server_remote_control"]:
            return
        message = json.loads(str(m))
        command = message["command"]
        if command != "ping":
            log_command.debug(command)
        if command == "switch":
            self.toggle_switch(message)
        if command == "coil":
            self.fire_coil(message)
        if command == "ball_search":
            ball.search()

    def toggle_switch(self, message):
        switch = p.switches[message["name"]]
        change_to = not switch.active
        if change_to:
            event = p.proc.SWITCH_OPENED if switch.opto else p.proc.SWITCH_CLOSED
        else:
            event = p.proc.SWITCH_CLOSED if switch.opto else p.proc.SWITCH_OPENED
        p.proc.artificial_events += [{"type": event, "value": switch.number}]

    def fire_coil(self, message):
        coil = p.coils[message["name"]]
        coil.pulse()


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

    def dispatch_notice(self, mtype, message):
        if not p.data["server_publish_events"]:
            return
        payload = { "message": "notice", "type": mtype, "text": message }
        cherrypy.engine.publish("websocket-broadcast", json.dumps(payload))

    def run(self):
        log.info("starting on port {}".format(port))
        plugin = WebSocketPlugin(cherrypy.engine)
        plugin.subscribe()
        cherrypy.tools.websocket = WebSocketTool()

        p.events.on("switch", self.dispatch_device)
        p.events.on("coil", self.dispatch_device)
        p.events.on("lamp", self.dispatch_device)
        p.events.on("flasher", self.dispatch_device)
        p.events.on("gi", self.dispatch_device)
        p.events.on("notice", self.dispatch_notice)

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
                "tools.websocket.handler_cls": WebSocketHandler
            }
        })
        self.done(plugin)

    def done(self, plugin):
        p.events.off("switch", self.dispatch_device)
        p.events.off("coil", self.dispatch_device)
        p.events.off("lamp", self.dispatch_device)
        p.events.off("flasher", self.dispatch_device)
        p.events.off("gi", self.dispatch_device)
        p.events.off("notice", self.dispatch_notice)

        plugin.unsubscribe()
        log.info("stopped")


class Mode(Handler):

    def setup(self):
        p.events.on("data_server_enabled", self.update)
        p.events.on("shutdown", self.disable)
        self.update()

    def update(self):
        global server
        if p.data["server_enabled"]:
            self.enable()
        else:
            self.disable()

    def on_enable(self):
        global server
        server = WebServer()
        server.start()

    def on_disable(self):
        global server
        cherrypy.engine.exit()
        server = None





