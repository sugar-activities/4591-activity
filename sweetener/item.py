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
from sugar.graphics.toolbutton import ToolButton

import stock


class Item(gobject.GObject):
    __gsignals__ = {'activate': (gobject.SIGNAL_RUN_LAST,
                                 gobject.TYPE_NONE,
                                 tuple())}
    toolitem = None

    def __init__(self, stock_id=gtk.STOCK_CLEAR, important=False):
        gobject.GObject.__init__(self)
        self._stock_id = stock_id
        self.accel_group = None
        self.important = important
        self.connection = None
        self.connection_data = None
        self.tooltip = None

    def set_stock_id(self, stock_id):
        self._stock_id = stock_id

    def get_stock_id(self):
        return self._stock_id

    stock_id = property(get_stock_id, set_stock_id)

    def get_menu_item(self):
        return None

    def activate_cb(self, widget):
        self.emit('activate')

    def setup_accelerator(self):
        accelerator = stock.get_accelerator(self._stock_id)
        logger.debug(str(accelerator))
        try:
            if accelerator[1] > 0:
                self.toolitem.props.accelerator = gtk.accelerator_name(
                    accelerator[1], accelerator[0])
        except:
            logger.error(
'Could not set up accelerator; if toogletoolbutton, update your sugar version')

    def get_tool_item(self):
        if self._stock_id in stock.icons:
            icon_name = stock.icons[self._stock_id]
        else:
            icon_name = self._stock_id
        sensitive = self.sensitive
        self.toolitem = ToolButton(icon_name)
        self.toolitem.connect('clicked', self.activate_cb)
        self.setup_tooltip()
        self.toolitem.set_sensitive(sensitive)
        return self.toolitem

    def setup_tooltip(self):
        if self.tooltip:
            self.toolitem.set_tooltip(self.tooltip)
        else:
            text = gtk.stock_lookup(self._stock_id)[1]
            self.toolitem.set_tooltip(text.replace('_', ''))
        self.setup_accelerator()

    def set_sensitive(self, setting):
        if self.toolitem:
            self.toolitem.set_sensitive(setting)

    def get_sensitive(self):
        if self.toolitem:
            return self.toolitem.get_sensitive()
        else:
            return True

    sensitive = property(get_sensitive, set_sensitive)
