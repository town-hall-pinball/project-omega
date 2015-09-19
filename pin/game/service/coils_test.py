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

import p
from pin.handler import Handler
from pin import dmd, ui, util

default_pulse_wait = 2.0
mode_labels = (
    "Manual",
    "Repeat",
    "Cycle",
)

class Mode(Handler):

    timer = None

    def setup(self):
        self.display = ui.Panel(name="coils_test")

        self.icon = ui.Image("service_coils", left=0)
        self.mode_label = ui.Text("Mode", font="t5cpb")
        self.name = ui.Text("Name", font="t5cp", case="full")
        self.pulse_label = ui.Text("Pulse", font="t5cp", fill=0x08,
                padding=[1, 5], enabled=False)

        ui.valign((self.mode_label, self.name, self.pulse_label))
        self.display.add((self.icon, self.mode_label, self.name,
                self.pulse_label))

        compare = lambda x, y: cmp(x.label, y.label)
        ordered_coils = sorted(p.coils.values(), cmp=compare)
        self.coils = util.Cycle(ordered_coils)
        self.modes = util.Cycle(mode_labels)

        self.on("switch_service_exit",  self.exit)
        self.on("switch_service_up", self.next)
        self.on("switch_service_down", self.previous)
        self.on("switch_service_enter", self.next_mode)
        self.on("switch_start_button", self.manual_pulse)

    def on_enable(self):
        self.update_mode()

    def on_disable(self):
        self.cancel(self.timer)

    def update_mode(self):
        mode = self.modes.get()
        self.mode_label.show(mode)
        self.update_selection()

    def update_selection(self):
        coil = self.coils.get()
        self.name.show(coil.label)
        if self.modes.get() in ("Repeat", "Cycle"):
            self.schedule_pulse()
        else:
            self.cancel(self.timer)

    def next(self):
        self.coils.next()
        self.update_selection()

    def previous(self):
        self.coils.previous()
        self.update_selection()

    def next_mode(self):
        mode = self.modes.next()
        self.update_mode()

    def schedule_pulse(self):
        self.cancel(self.timer)
        self.timer = self.wait(default_pulse_wait, self.scheduled_pulse)

    def scheduled_pulse(self):
        if self.modes.get() == "Cycle":
            self.coils.next()
        coil = self.coils.get()
        self.name.show(coil.label)
        self.pulse()
        self.schedule_pulse()

    def manual_pulse(self):
        if self.modes.get() == "Manual":
            self.pulse()

    def pulse(self):
        self.coils.get().pulse()
        self.pulse_label.show("Pulse", 1.0)

    def exit(self):
        self.disable()
        p.mixer.play("service_exit")

    def on_disable(self):
        p.modes["service"].resume()
