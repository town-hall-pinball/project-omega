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

from collections import deque

import p
from pin import ui, util
from pin.handler import Handler
from ..config import service_menu as menu

def option_tuple(option):
    if isinstance(option, list):
        value = option[0]
        text = option[1]
    else:
        value = option
        text = option
    return (value, text)


def text_for_value(options, search):
    for option in options:
        value, text = option_tuple(option)
        if search == value:
            return text


def index_for_value(options, search):
    index = 0
    for option in options:
        value, text = option_tuple(option)
        if search == value:
            return index
        index += 1

class MenuNode(object):

    def __init__(self, key, node):
        self.key = key
        self.node = node
        self.type = None
        if "options" in node:
            self.type = "edit"
            self.items = node["options"]
        else:
            item = node["menu"][0]
            if "icon" in item:
                self.type = "icon"
                self.items = node["menu"]
            elif "options" in item:
                self.type = "option"
                self.items = node["menu"]
            elif "data" in item:
                self.type = "value"
                self.items = node["menu"]
            else:
                self.type = "text"
                self.items = node["menu"]
        self.iter = util.Cycle(self.items)


class Mode(Handler):

    def setup(self):
        self.menus = {}
        self.key_stack = deque()
        self.menu_stack = deque()
        self.depth = 0

        self.breadcrumbs = ui.Text(left=2, top=1, font="t5cd")
        self.name = ui.Text("Settings", top=1)
        self.value = ui.Text(top=12, padding=[1, 5])
        self.icons = ui.Panel(top=5, fill=None)
        self.icons.add(ui.Image("service_settings"))
        self.default = ui.Text(bottom=2, right=2, font="t5cd")
        self.result = ui.Text(bottom=2, fill=0x2, padding=[1, 3], font="t5cpb")

        self.panel = ui.Panel(name="root")
        self.panel.add([self.breadcrumbs, self.name, self.value, self.icons,
                self.default, self.result])

        self.result_timer = None

        self.on("switch_service_enter", self.enter)
        self.on("switch_service_up",    self.up)
        self.on("switch_service_down",  self.down)
        self.on("switch_service_exit",  self.exit)

    def push_menu(self, node):
        self.depth += 1
        self.key_stack += [node.get("name", "/")]
        key = "/".join(self.key_stack)
        if key in self.menus:
            self.menu = self.menus[key]
        else:
            self.menu = MenuNode(key, node)
            self.menus[key] = self.menu
        self.menu_stack += [self.menu]
        self.new_menu()

    def new_menu(self):
        self.breadcrumbs.show("<" * self.depth)
        self.name.hide()
        self.value.hide()
        self.icons.clear()
        if self.menu.type == "icon":
            for item in self.menu.items:
                icon = ui.Image(item["icon"],
                    padding=[0, 1]
                )
                self.icons.add(icon)
            ui.halign(self.icons.children)
        elif self.menu.type == "edit":
            options = self.menu.node["options"]
            key = self.menu.node["data"]
            self.menu.iter.index = index_for_value(options, p.data[key])
        self.update()

    def enabled(self):
        self.push_menu(menu.main)
        p.dmd.clear()
        p.dmd.stack("service", self.panel)

    def disabled(self):
        p.dmd.remove("service")

    def enter(self):
        item = self.menu.iter.get()
        if not isinstance(item, list) and item.get("confirm", False):
            raise ValueError("a")
        elif self.menu.type == "edit":
            self.save()
        elif "menu" in item or "options" in item:
            p.mixer.play("service_enter")
            self.push_menu(item)
        elif "action" in item:
            p.mixer.play("service_enter")
            getattr(self, item["action"])()

    def exit(self):
        self.pop_menu()

    def pop_menu(self):
        self.depth -= 1
        self.key_stack.pop()
        self.menu_stack.pop()
        if self.depth == 0:
            p.modes["attract"].enable()
            self.disable()
        else:
            p.mixer.play("service_exit")
            self.menu = self.menu_stack[-1]
            self.new_menu()

    def up(self):
        p.mixer.play("service_select")
        self.menu.iter.next()
        self.update()

    def down(self):
        p.mixer.play("service_select")
        self.menu.iter.previous()
        self.update()

    def update(self):
        menu = self.menu
        selected = menu.iter.get()
        self.default.hide()
        self.value.hide()
        self.value.update(fill=None)

        if menu.type == "text":
            self.name.show(self.menu.node.get("name", ""))
            self.value.show(selected["name"])
        elif menu.type == "icon":
            self.name.show(selected["name"])
            for i in xrange(len(menu.items)):
                fill = 0xf if i == menu.iter.index else 0
                reverse = i == menu.iter.index
                self.icons.children[i].update(fill=fill, reverse=reverse)
        elif menu.type == "option":
            self.name.show(selected["name"])
            value = p.data[selected["data"]]
            default_value = p.defaults[selected["data"]]
            text = text_for_value(selected["options"], value)
            self.value.show(text)
            if value != None and value == default_value:
                self.default.show("Default")
        elif menu.type == "edit":
            self.name.show(menu.node["name"])
            value = selected[0]
            default_value = p.defaults[menu.node["data"]]
            self.value.show(selected[1])
            self.value.update(fill=0x4)
            if value != None and value == default_value:
                self.default.show("Default")
        elif menu.type == "value":
            self.name.show(selected["name"])
            value = p.data[selected["data"]]
            if "format" in selected:
                value = selected["format"].format(value)
            self.value.show(str(value))

    def save(self):
        item = self.menu.iter.get()
        key = self.menu.node["data"]
        value, text = option_tuple(item)
        self.result.enabled = True
        if value != p.data[key]:
            p.data[key] = value
            p.data.save()
            self.result.show("Saved")
            p.mixer.play("service_save")
        else:
            self.result.show("No Change")
            p.mixer.play("service_exit")
        self.pop_menu()

        self.cancel(self.result_timer)
        self.result_timer = self.wait(1.0, self.clear_result)

    def clear_result(self):
        self.result.hide()

    def animation_browser(self):
        p.modes["animation_browser"].enable()



