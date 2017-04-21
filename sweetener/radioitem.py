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
import gtk
from sugar.graphics.radiotoolbutton import RadioToolButton
import stock
from toggleitem import ToggleItem


class RadioItem(ToggleItem):
    def __init__(self, group, default_value=True,
                  stock_id=None, important=False):
        ToggleItem.__init__(self, default_value, stock_id, important)
        self.group = group

    def get_tool_item(self):
        self.toolitem = RadioToolButton()
        if self.group:
            self.toolitem.set_group(self.group.toolitem)
        self.toolitem.set_named_icon(stock.icons[self._stock_id]
                                     if self._stock_id in stock.icons
                                     else self._stock_id)
        self.toolitem.set_active(self.default_value)
        self.toolitem.connect('toggled', self.toggled_cb)
        self.setup_tooltip()
        return self.toolitem
