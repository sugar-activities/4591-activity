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

import logging
logger = logging.getLogger('option')

import gobject
import gtk

from sugar.graphics.colorbutton import ColorToolButton

from colors import color2string
from item import Item


class ColorItem(Item):
    __gsignals__ = {'updated': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                                (gobject.TYPE_STRING,))}

    def __init__(self, parent=None, important=False):
        Item.__init__(self, gtk.STOCK_SELECT_COLOR)
        self.color = '#FFFFFF'

    def set_color(self, color):
        self.color = color
        if self.toolitem and self.color:
            self.toolitem.set_color(gtk.gdk.Color(self.color))

    def get_tool_item(self):
        self.toolitem = ColorToolButton()
        self.toolitem.connect('notify::color', self._color_changed_cb)
        self.setup_tooltip()
        self.set_color(self.color)
        return self.toolitem

    def setup_tooltip(self):
        if self.tooltip:
            self.toolitem.set_title(self.tooltip)
        else:
            text = gtk.stock_lookup(self.stock_id)[1]
            self.toolitem.set_title(text.replace('_', ''))
        self.setup_accelerator()

    def _color_changed_cb(self, widget, pspec):
        color_gdk = widget.get_color()
        self.color = color2string(color_gdk)
        self.emit('updated', self.color)
