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

from ..lib.handler import Handler
from ..lib import p, dmd, ui, util

mode_labels = (
    "Manual",
    "Repeat",
    "Cycle",
)

class PulseTest(Handler):

    timer = None

    def __init__(self, name, icon, devices):
        self.image = ui.Image(icon, left=0)
        self.devices = util.Cycle(devices)
        self.interval = 2.0
        super(PulseTest, self).__init__(name)

    def setup(self):
        self.display = ui.Panel(name=self.name)

        self.mode_label = ui.Text("Mode", font="t5b")
        self.name_label = ui.Text("Name", font="t5cp", case="full")
        self.action_label = ui.Text("Action", font="t5cp", fill=0x08,
                padding=[1, 5], enabled=False)

        ui.valign((self.mode_label, self.name_label, self.action_label))
        self.display.add((self.image, self.mode_label, self.name_label,
                self.action_label))
        self.modes = util.Cycle(mode_labels)

        self.on("switch_service_exit",  self.exit)
        self.on("switch_service_up", self.next)
        self.on("switch_service_down", self.previous)
        self.on("switch_service_enter", self.next_mode)
        self.on("switch_start_button", self.manual_action)

    def on_enable(self):
        self.update_mode()

    def on_disable(self):
        self.cancel(self.timer)

    def update_mode(self):
        mode = self.modes.get()
        self.mode_label.show(mode)
        self.update_selection()

    def update_selection(self):
        device = self.devices.get()
        self.name_label.show(device.label)
        if self.modes.get() in ("Repeat", "Cycle"):
            self.schedule_action()
        else:
            self.cancel(self.timer)

    def next(self):
        p.mixer.play("service_select")
        self.devices.get().disable()
        self.devices.next()
        self.update_selection()

    def previous(self):
        p.mixer.play("service_select")
        self.devices.get().disable()
        self.devices.previous()
        self.update_selection()

    def next_mode(self):
        p.mixer.play("service_enter")
        mode = self.modes.next()
        self.update_mode()

    def schedule_action(self):
        self.cancel(self.timer)
        self.timer = self.wait(self.interval, self.scheduled_action)

    def scheduled_action(self):
        if self.modes.get() == "Cycle":
            self.devices.next()
        device = self.devices.get()
        self.name_label.show(device.label)
        self.pulse()
        self.schedule_action()

    def pulse(self):
        self.devices.get().pulse()
        self.action_label.show("Pulse", 1.0)

    def manual_action(self):
        if self.modes.get() == "Manual":
            self.pulse()

    def exit(self):
        self.disable()
        p.mixer.play("service_exit")

    def on_disable(self):
        p.modes["service"].resume()
