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


def text_for_value(options, search):
    for option in options:
        value, text = option
        if search == value:
            return text


def index_for_value(options, search):
    index = 0
    for option in options:
        value, text = option
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

        self.question = ui.Panel(fill=None, enabled=False)
        self.confirm = ui.Text("Confirm?", bottom=2, padding=[1,4], font="t5cpb")
        self.yes = ui.Text("YES", bottom=2, padding=[1,4], font="t5cpb")
        self.no = ui.Text("NO", bottom=2, padding=[1,4], font="t5cpb")
        self.question.add((self.confirm, self.yes, self.no))
        ui.halign((self.confirm, self.yes, self.no))
        self.confirmed = None

        self.display = ui.Panel(name="service")
        self.display.add([self.breadcrumbs, self.name, self.value, self.icons,
                self.default, self.result, self.question])

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

    def on_enable(self):
        p.modes["attract"].suspend()
        self.push_menu(menu.main)
        p.dmd.clear()

    def enter(self):
        if self.confirmed:
            self.select_confirmed()
            return
        item = self.menu.iter.get()
        if not isinstance(item, list) and item.get("confirm", False):
            self.start_confirmed()
        elif self.menu.type == "edit":
            self.save()
        elif "menu" in item or "options" in item:
            p.mixer.play("service_enter")
            self.push_menu(item)
        elif "action" in item:
            p.mixer.play("service_enter")
            getattr(self, item["action"])()

    def exit(self):
        if self.confirmed is None:
            self.pop_menu()
        else:
            self.cancel_confirmed()

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
        if self.confirmed is None:
            self.menu.iter.next()
            self.update()
        else:
            self.confirmed.next()
            self.update_confirmed()

    def down(self):
        p.mixer.play("service_select")
        if self.confirmed is None:
            self.menu.iter.previous()
            self.update()
        else:
            self.confirmed.previous()
            self.update_confirmed()

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
        value, text = item
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

    def start_confirmed(self):
        self.confirmed = util.Cycle((False, True))
        p.mixer.play("service_enter")
        self.question.show()
        self.update_confirmed()

    def update_confirmed(self):
        if self.confirmed.get():
            self.yes.update(color=0x0, fill=0xf)
            self.no.update(color=0xf, fill=0x0)
        else:
            self.yes.update(color=0xf, fill=0x0)
            self.no.update(color=0x0, fill=0xf)

    def cancel_confirmed(self):
        self.confirmed = None
        self.question.hide()
        p.mixer.play("service_cancel")
        self.result.show("Cancelled")
        self.cancel(self.result_timer)
        self.result_timer = self.wait(1.0, self.clear_result)

    def select_confirmed(self):
        if self.confirmed.get():
            self.confirmed = None
            self.question.hide()
            p.mixer.play("service_save")
            self.result.show("Confirmed")
            self.cancel(self.result_timer)
            self.result_timer = self.wait(1.0, self.clear_result)
            item = self.menu.iter.get()
            getattr(self, item["action"])()
        else:
            self.cancel_confirmed()

    def on_suspend(self):
        self.unregister()

    def on_resume(self):
        self.register()

# =============
# Actions
# =============

    def clear_credits(self):
        p.data["credits"] = 0
        p.data.save()

    def movie_browser(self):
        p.modes["movie_browser"].enable()
        self.suspend()

    def music_browser(self):
        p.modes["music_browser"].enable()
        self.suspend()

    def sound_browser(self):
        p.modes["sound_browser"].enable()
        self.suspend()

    def font_browser(self):
        p.modes["font_browser"].enable()
        self.suspend()

    def image_browser(self):
        p.modes["image_browser"].enable()
        self.suspend()

    def switch_edges_test(self):
        p.modes["switch_edges_test"].enable()
        self.suspend()

    def switch_levels_test(self):
        p.modes["switch_levels_test"].enable()
        self.suspend()

    def switch_single_test(self):
        p.modes["switch_single_test"].enable()
        self.suspend()

    def coils_test(self):
        p.modes["coils_test"].enable()
        self.suspend()

    def lamps_all_test(self):
        p.modes["lamps_all_test"].enable()
        self.suspend()

    # --------
    # Startup
    # --------

    def direct_start(self):

        def start(resource):
            p.modes["service"].enable()
            p.modes["service"].suspend()
            p.modes[resource + "_browser"].enable()
            p.modes[resource + "_browser"].select(p.options[resource])

        if p.options["font"]:
            start("font")
            return True
        if p.options["image"]:
            start("image")
            return True
        if p.options["movie"]:
            start("movie")
            return True
        if p.options["music"]:
            start("music")
            return True
        if p.options["sound"]:
            start("sound")
            return True

        return False





