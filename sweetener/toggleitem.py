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
logger = logging.getLogger('toggleoption')
import gobject
import gtk
from sugar.graphics.toggletoolbutton import ToggleToolButton
import stock
from item import Item


class ToggleItem(Item):
    __gsignals__ = {'toggled': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                                (gobject.TYPE_BOOLEAN,))}

    def __init__(self, default_value=True, stock_id=None, important=False):
        Item.__init__(self, stock_id, important)
        self.default_value = default_value
        self.active = default_value

    def get_menu_item(self):
        return None

    def toggled_cb(self, widget):
        active = widget.get_active()
        self.toolitem.set_active(active)
        self.active = active
        self.emit('toggled', active)

    def get_tool_item(self):
        self.toolitem = ToggleToolButton()
        self.toolitem.set_named_icon(stock.icons[self._stock_id]
                                     if self._stock_id in stock.icons
                                     else self._stock_id)
        self.toolitem.set_active(self.default_value)
        self.toolitem.connect('toggled', self.toggled_cb)
        self.setup_tooltip()
        return self.toolitem
