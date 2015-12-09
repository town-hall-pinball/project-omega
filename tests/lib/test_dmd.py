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

import pygame

from pin.lib import p, devices, dmd, ui
import unittest
from tests import fixtures
from mock import Mock, patch

class TestDMD(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.r1 = Mock(ui.Panel)
        self.r2 = Mock(ui.Panel)
        self.r3 = Mock(ui.Panel)
        self.trans = Mock(ui.transition.Transition)
        self.trans.done = False

    def test_add(self):
        dmd.add(self.r1)
        dmd.render()
        self.assertEquals(1, self.r1.render.call_count)

    def test_add_once(self):
        dmd.add(self.r1)
        dmd.add(self.r1)
        dmd.render()
        self.assertEquals(1, self.r1.render.call_count)

    def test_enqueue(self):
        dmd.add(self.r1)
        dmd.enqueue(self.r2)
        dmd.render()
        self.assertEquals(0, self.r1.render.call_count)
        self.assertEquals(1, self.r2.render.call_count)

    def test_enqueue_once(self):
        dmd.enqueue(self.r1)
        dmd.enqueue(self.r1)
        self.assertEquals(1, len(dmd.dmd.queue))

    def test_interrupt(self):
        dmd.add(self.r1)
        dmd.interrupt(self.r2)
        dmd.render()
        self.assertEquals(0, self.r1.render.call_count)
        self.assertEquals(1, self.r2.render.call_count)

    def test_interrupt_remove(self):
        dmd.add(self.r1)
        dmd.interrupt(self.r2)
        dmd.remove(self.r2)
        dmd.render()
        self.assertEquals(1, self.r1.render.call_count)
        self.assertEquals(0, self.r2.render.call_count)

    def test_replace_stack(self):
        dmd.add(self.r1)
        dmd.replace(self.r1, self.r2)
        dmd.render()
        self.assertEquals(0, self.r1.render.call_count)
        self.assertEquals(1, self.r2.render.call_count)

    def test_replace_queue(self):
        dmd.enqueue(self.r1)
        dmd.replace(self.r1, self.r2)
        dmd.render()
        self.assertEquals(0, self.r1.render.call_count)
        self.assertEquals(1, self.r2.render.call_count)

    def test_replace_none(self):
        dmd.replace(self.r1, self.r2)
        dmd.render()
        self.assertEquals(0, self.r1.render.call_count)
        self.assertEquals(1, self.r2.render.call_count)

    def test_dequeue(self):
        dmd.add(self.r1)
        dmd.enqueue(self.r2)
        dmd.render()
        dmd.remove(self.r2)
        dmd.render()
        self.assertEquals(1, self.r1.render.call_count)
        self.assertEquals(1, self.r2.render.call_count)

    def test_clear(self):
        dmd.add(self.r1)
        dmd.enqueue(self.r2)
        dmd.clear()
        dmd.render()
        self.assertEquals(1, self.r1.render.call_count)
        self.assertEquals(0, self.r2.render.call_count)

    def test_reset(self):
        dmd.add(self.r1)
        dmd.enqueue(self.r2)
        dmd.reset()
        self.assertFalse(dmd.render())

    def test_transition(self):
        dmd.add(self.r1)
        dmd.replace(self.r1, self.r2, self.trans)
        dmd.render()
        self.assertEquals(1, self.r1.render.call_count)
        self.assertEquals(1, self.r2.render.call_count)

    def test_render_start(self):
        dmd.add(self.r1)
        dmd.render()
        self.assertEquals(1, self.r1.render_start.call_count)

    def test_render_stop(self):
        dmd.add(self.r1)
        dmd.render()
        dmd.remove(self.r1)
        self.assertEquals(1, self.r1.render_start.call_count)
        self.assertEquals(1, self.r1.render_stop.call_count)

    def test_render_suspend(self):
        dmd.add(self.r1)
        dmd.enqueue(self.r2)
        dmd.render()
        self.assertEquals(1, self.r1.render_suspend.call_count)

    def test_render_suspend_with_transition(self):
        dmd.add(self.r1, self.trans)
        dmd.add(self.r2, self.trans)
        dmd.enqueue(self.r3)
        dmd.render()
        self.assertEquals(1, self.r2.render_suspend.call_count)

    def test_render_stop_with_transition(self):
        dmd.add(self.r1)
        dmd.add(self.r2, self.trans)
        dmd.remove(self.r1)
        dmd.render()
        self.assertTrue(self.r1.render_stop.call_count > 0)

    def test_render_resume(self):
        dmd.add(self.r1)
        dmd.enqueue(self.r2)
        dmd.remove(self.r2)
        dmd.render()
        self.assertEquals(2, self.r1.render_start.call_count)

    def test_transition_done(self):
        dmd.add(self.r1)
        dmd.add(self.r2, self.trans)
        self.trans.done = True
        dmd.render()
        self.assertTrue(self.r1.render_stop.call_count > 0)

    @patch("pygame.Surface")
    def test_create_frame(self, mock_surface):
        dmd.create_frame(10, 20, has_alpha=False)
        mock_surface.assert_called_with((10, 20))

    @patch("pygame.Surface")
    def test_create_frame_alpha(self, mock_surface):
        dmd.create_frame(10, 20)
        mock_surface.assert_called_with((10, 20), pygame.locals.SRCALPHA)

    @patch("pygame.PixelArray")
    def test_create_dots(self, mock_pixel_array):
        dmd.create_dots(None)

    def test_no_renderer(self):
        with self.assertRaises(ValueError):
            dmd.dmd.stack += [None]
            dmd.render()


