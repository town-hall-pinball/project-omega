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

import socket
import json

from pin.lib import p, server

import unittest
from mock import Mock, patch
from tests import fixtures

class TestRoot(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.root = server.Root()

    def test_ws(self):
        self.root.ws()

    def test_branding(self):
        brand = self.root.branding()
        self.assertEquals("Project Omega", brand["name"])

    def test_status(self):
        status = self.root.status()
        self.assertEquals(status["devices"]["C02"]["name"], "auto_plunger")
        self.assertEquals(status["devices"]["C25"]["name"], "auto_fire")
        self.assertEquals(status["devices"]["L86"]["name"], "ball_launch_button")
        self.assertEquals(status["devices"]["S11"]["name"], "ball_launch_button")


class TestWebSocketHandler(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.ws = server.WebSocketHandler(Mock(spec=socket.socket))
        p.data["server_remote_control"] = True

    def test_ping(self):
        self.ws.received_message('{ "command": "ping" }')

    def test_switch_activate(self):
        self.ws.received_message('{ "command": "switch", "name": "start_button" }')
        fixtures.loop()
        self.assertTrue(p.switches["start_button"].active)

    def test_switch_deactivate(self):
        p.switches["start_button"].active = True
        self.ws.received_message('{ "command": "switch", "name": "start_button" }')
        fixtures.loop()
        self.assertFalse(p.switches["start_button"].active)

    def test_coil(self):
        listener = Mock()
        p.events.on("coil_trough", listener)
        self.ws.received_message('{ "command": "coil", "name": "trough" }')
        fixtures.loop()
        self.assertTrue(listener.called)

    @patch("pin.lib.search.run")
    def test_ball_search(self, mock):
        self.ws.received_message('{ "command": "ball_search" }')
        fixtures.loop()
        self.assertTrue(mock.called)

    def test_no_switch_activate(self):
        p.data["server_remote_control"] = False
        self.ws.received_message('{ "command": "switch", "name": "start_button" }')
        fixtures.loop()
        self.assertFalse(p.switches["start_button"].active)


class TestWebServer(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.ws = server.WebServer()

    @patch("cherrypy.quickstart")
    def test_run(self, mock):
        self.ws.run()

    def to_message(self, item):
        payload = item.__dict__
        payload["message"] = item.type
        return json.dumps(payload)

    @patch("cherrypy.quickstart")
    @patch("cherrypy.engine.publish")
    def test_dispatch_switch(self, mock_publish, mock_start):
        p.data["server_publish_events"] = True
        self.ws.done = Mock()
        self.ws.run()
        switch = p.switches["start_button"]
        switch.activate()
        fixtures.loop()

        mock_publish.assert_called_with("websocket-broadcast",
                self.to_message(switch))

    @patch("cherrypy.quickstart")
    @patch("cherrypy.engine.publish")
    def test_dispatch_coil(self, mock_publish, mock_start):
        p.data["server_publish_events"] = True
        self.ws.done = Mock()
        self.ws.run()
        coil = p.coils["trough"]
        coil.enable()
        fixtures.loop()

        mock_publish.assert_called_with("websocket-broadcast",
                self.to_message(coil))

    @patch("cherrypy.quickstart")
    @patch("cherrypy.engine.publish")
    def test_dispatch_lamp(self, mock_publish, mock_start):
        p.data["server_publish_events"] = True
        self.ws.done = Mock()
        self.ws.run()
        lamp = p.lamps["start_button"]
        lamp.enable()
        fixtures.loop()

        mock_publish.assert_called_with("websocket-broadcast",
                self.to_message(lamp))

    @patch("cherrypy.quickstart")
    @patch("cherrypy.engine.publish")
    def test_dispatch_flasher(self, mock_publish, mock_start):
        p.data["server_publish_events"] = True
        self.ws.done = Mock()
        self.ws.run()
        flasher = p.flashers["auto_fire"]
        flasher.enable()
        fixtures.loop()

        mock_publish.assert_called_with("websocket-broadcast",
                self.to_message(flasher))

    @patch("cherrypy.quickstart")
    @patch("cherrypy.engine.publish")
    def test_dispatch_flasher(self, mock_publish, mock_start):
        p.data["server_publish_events"] = True
        self.ws.done = Mock()
        self.ws.run()
        gi = p.gi["gi01"]
        gi.enable()
        fixtures.loop()

        mock_publish.assert_called_with("websocket-broadcast",
                self.to_message(gi))

    @patch("cherrypy.quickstart")
    @patch("cherrypy.engine.publish")
    def test_no_dispatch_switch(self, mock_publish, mock_start):
        p.data["server_publish_events"] = False
        self.ws.done = Mock()
        self.ws.run()
        switch = p.switches["start_button"]
        switch.activate()
        fixtures.loop()
        self.assertFalse(mock_publish.called)

    @patch("cherrypy.quickstart")
    @patch("cherrypy.engine.publish")
    def test_notice(self, mock_publish, mock_start):
        p.data["server_publish_events"] = True
        self.ws.done = Mock()
        self.ws.run()
        p.events.post("notice", "foo", "bar")
        fixtures.loop()

        payload = { "message": "notice", "type": "foo", "text": "bar" }
        message = json.dumps(payload)
        mock_publish.assert_called_with("websocket-broadcast", message)

    @patch("cherrypy.quickstart")
    @patch("cherrypy.engine.publish")
    def test_no_notice(self, mock_publish, mock_start):
        p.data["server_publish_events"] = False
        self.ws.done = Mock()
        self.ws.run()
        p.events.post("notice", "foo", "bar")
        fixtures.loop()
        self.assertFalse(mock_publish.called)


class TestMode(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.mode = server.Mode("server")

    @patch("cherrypy.engine.exit")
    @patch("pin.lib.server.WebServer")
    def test_toggle(self, mock_server, mock_exit):
        p.data["server_enabled"] = True
        fixtures.loop()
        self.assertTrue(self.mode.enabled)
        p.data["server_enabled"] = False
        fixtures.loop()
        self.assertFalse(self.mode.enabled)

