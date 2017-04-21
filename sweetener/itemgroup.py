#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 S. Daniel Francis <francis@sugarlabs.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

import gobject
import gtk
from sugar.activity.widgets import ToolbarButton


class ItemGroup(gobject.GObject):
    def __init__(self, box, name=None, icon=None):
        gobject.GObject.__init__(self)
        self.items = []
        self.item = ToolbarButton(icon_name=icon)
        box.toolbar.insert(self.item, len(box.toolbar) - 2)
        self.toolbar = gtk.Toolbar()
        self.item.props.page = self.toolbar
        self.toolbar.show()
        self.item.show()
        self.activity = box._parent
        self.last_position = 0

    def append_item(self, item):
        tool_item = item.get_tool_item()
        self.toolbar.insert(tool_item, len(self.items) - self.last_position)
        tool_item.show_all()
        self.items.append(item)

    def append_separator(self, important=False):
        toolitem = gtk.SeparatorToolItem()
        toolitem.show()
        self.toolbar.insert(toolitem, len(self.items) - self.last_position)
        self.items.append(self.toolbar)
        return toolitem


class GhostGroup(ItemGroup):
    def __init__(self, box, name):
        gobject.GObject.__init__(self)
        self.items = [i for i in box.toolbar.get_children()[:-2]]
        self.toolbar = box.toolbar
        self.activity = box._parent
        self.last_position = 0


class SubGroup(ItemGroup):
    def __init__(self, group, name=None):
        gobject.GObject.__init__(self)
        self.items = group.items
        self.last_position = group.last_position
        if len(self.items) > 0:
            group.append_separator()
        group.append_separator()
        self.toolbar = group.toolbar
        self.last_position = 1
