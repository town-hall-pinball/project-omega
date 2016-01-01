# Copyright (c) 2014 - 2016 townhallpinball.org
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

import pygame
from pin.lib import p, keyboard

from mock import Mock, patch
import unittest
from tests import fixtures

class TestKeyboard(unittest.TestCase):
    """
    Note: pygame.key.name needs to be patched as it returns "unknown" for
    every key until the display is initialized
    """

    def setUp(self):
        fixtures.reset()

    @patch("pygame.event.get")
    @patch("pygame.key.name")
    def test_event(self, name, keys):
        name.return_value = "a"
        keys.return_value = [pygame.event.Event(pygame.locals.KEYDOWN, {
            "key": pygame.locals.K_a,
        })]
        listener = Mock()
        p.events.on("a_event", listener)
        keyboard.register({"a": keyboard.event("a_event", foo=1)})
        keyboard.process()
        p.events.dispatch()
        listener.assert_called_with(foo=1)

    @patch("pygame.event.get")
    @patch("pygame.key.name")
    def test_event_with_shift(self, name, keys):
        pygame.key.get_mods.return_value = pygame.locals.KMOD_LSHIFT
        name.return_value = "a"
        keys.return_value = [pygame.event.Event(pygame.locals.KEYDOWN, {
            "key": pygame.locals.K_a,
        })]
        listener = Mock()
        p.events.on("a_event", listener)
        keyboard.register({"sa": keyboard.event("a_event", foo=1)})
        keyboard.process()
        p.events.dispatch()
        listener.assert_called_with(foo=1)

    @patch("pygame.event.get")
    @patch("pygame.key.name")
    def test_event_with_control(self, name, keys):
        pygame.key.get_mods.return_value = pygame.locals.KMOD_LCTRL
        name.return_value = "a"
        keys.return_value = [pygame.event.Event(pygame.locals.KEYDOWN, {
            "key": pygame.locals.K_a,
        })]
        listener = Mock()
        p.events.on("a_event", listener)
        keyboard.register({"ca": keyboard.event("a_event", foo=1)})
        keyboard.process()
        p.events.dispatch()
        listener.assert_called_with(foo=1)

    @patch("pygame.event.get")
    @patch("pygame.key.name")
    def test_event_with_alt(self, name, keys):
        pygame.key.get_mods.return_value = pygame.locals.KMOD_LALT
        name.return_value = "a"
        keys.return_value = [pygame.event.Event(pygame.locals.KEYDOWN, {
            "key": pygame.locals.K_a,
        })]
        listener = Mock()
        p.events.on("a_event", listener)
        keyboard.register({"aa": keyboard.event("a_event", foo=1)})
        keyboard.process()
        p.events.dispatch()
        listener.assert_called_with(foo=1)

    @patch("pygame.event.get")
    @patch("pygame.key.name")
    def test_switch_active(self, name, events):
        name.return_value = "a"
        events.return_value = [pygame.event.Event(pygame.locals.KEYDOWN, {
            "key": pygame.locals.K_a,
        })]
        keyboard.register({"a": keyboard.switch("start_button")})
        keyboard.process()
        event = p.proc.artificial_events[0]
        self.assertEquals(event["type"], p.proc.SWITCH_CLOSED)
        self.assertTrue(event["value"], p.switches["start_button"].number)

    @patch("pygame.event.get")
    @patch("pygame.key.name")
    def test_switch_inactive(self, name, events):
        name.return_value = "a"
        events.return_value = [pygame.event.Event(pygame.locals.KEYUP, {
            "key": pygame.locals.K_a,
        })]
        keyboard.register({"a": keyboard.switch("start_button")})
        keyboard.process()
        event = p.proc.artificial_events[0]
        self.assertEquals(event["type"], p.proc.SWITCH_OPENED)
        self.assertTrue(event["value"], p.switches["start_button"].number)

    @patch("pygame.event.get")
    @patch("pygame.key.name")
    def test_switch_inactive_active_only(self, name, events):
        name.return_value = "a"
        events.return_value = [pygame.event.Event(pygame.locals.KEYUP, {
            "key": pygame.locals.K_a,
        })]
        keyboard.register({"a": keyboard.switch("start_button",
                active_only=True)})
        keyboard.process()
        self.assertEquals(0, len(p.proc.artificial_events))

    @patch("pygame.event.get")
    @patch("pygame.key.name")
    def test_opto_active(self, name, events):
        name.return_value = "a"
        events.return_value = [pygame.event.Event(pygame.locals.KEYDOWN, {
            "key": pygame.locals.K_a,
        })]
        keyboard.register({"a": keyboard.switch("trough")})
        keyboard.process()
        event = p.proc.artificial_events[0]
        self.assertEquals(event["type"], p.proc.SWITCH_OPENED)
        self.assertTrue(event["value"], p.switches["trough"].number)

    @patch("pygame.event.get")
    @patch("pygame.key.name")
    def test_opto_inactive(self, name, events):
        name.return_value = "a"
        events.return_value = [pygame.event.Event(pygame.locals.KEYUP, {
            "key": pygame.locals.K_a,
        })]
        keyboard.register({"a": keyboard.switch("trough")})
        keyboard.process()
        event = p.proc.artificial_events[0]
        self.assertEquals(event["type"], p.proc.SWITCH_CLOSED)
        self.assertTrue(event["value"], p.switches["trough"].number)

    @patch("pygame.event.get")
    @patch("pygame.key.name")
    def test_reset(self, name, events):
        name.return_value = "a"
        events.return_value = [pygame.event.Event(pygame.locals.KEYDOWN, {
            "key": pygame.locals.K_a,
        })]
        listener = Mock()
        p.events.on("a_event", listener)
        keyboard.register({"a": keyboard.event("a_event")})
        keyboard.reset()
        keyboard.process()
        p.events.dispatch()
        self.assertFalse(listener.called)


