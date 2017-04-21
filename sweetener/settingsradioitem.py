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
from radioitem import RadioItem
from settingsitem import SettingsItem


class SettingsRadioItem(SettingsItem, RadioItem):
    __gsignals__ = {'toggled': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                                (gobject.TYPE_BOOLEAN,))}

    def __init__(self, group, default_value=True, parent=None,
                 stock_id=None, important=False):
        SettingsItem.__init__(self, parent, stock_id, important)
        RadioItem.__init__(self, group, default_value, stock_id, important)

    def get_tool_item(self):
        RadioItem.get_tool_item(self)
        self.toolitem.connect('clicked', self.activate_cb)
        self.palette = self.toolitem.get_palette()
        self.palette.set_content(self.content)
        self.content.show_all()
        return self.toolitem
