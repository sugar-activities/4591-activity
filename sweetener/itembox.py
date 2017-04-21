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

import gtk
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import StopButton


class ItemBox(ToolbarBox):
    def __init__(self, activity):
        ToolbarBox.__init__(self)
        self._parent = activity
        separator = gtk.SeparatorToolItem()
        separator.set_draw(False)
        separator.set_expand(True)
        separator.show()
        self.toolbar.insert(separator, -1)
        self.stopbutton = StopButton(activity)
        self.toolbar.insert(self.stopbutton, -1)
        self.stopbutton.show()
