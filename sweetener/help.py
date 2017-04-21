# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 S. Daniel Francis <francis@sugarlabs.org>
# Based on helpbutton by Gonzalo Odiard <gonzalo@laptop.org>
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

from gettext import gettext as _
import gtk

from sugar.graphics import style
from sugar.graphics.icon import Icon

import stock
from settingsitem import SettingsItem
from itemgroup import ItemGroup
import info
import helpcontent


class Help(SettingsItem):
    def __init__(self, box):
        title = gtk.stock_lookup(gtk.STOCK_HELP)[1]
        stock.register('sweetener-help-contents', title,
                       '<Ctrl>H', 'toolbar-help')
        SettingsItem.__init__(self, None, 'sweetener-help-contents')

        sw = gtk.ScrolledWindow()
        sw.set_size_request(int(gtk.gdk.screen_width() / 2.8),
            gtk.gdk.screen_height() - style.GRID_CELL_SIZE * 3)
        sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self._max_text_width = int(gtk.gdk.screen_width() / 3) - 20
        self._vbox = gtk.VBox()
        self._vbox.set_homogeneous(False)
        hbox = gtk.HBox()
        hbox.pack_start(self._vbox, False, True, 0)
        sw.add_with_viewport(hbox)
        sw.show()
        self.content = sw
        item = self.get_tool_item()
        item.show_all()
        separator = gtk.SeparatorToolItem()
        separator.show()
        box.toolbar.insert(separator,
                           len(box.toolbar.get_children()[:-2]))
        box.toolbar.insert(item,
                           len(box.toolbar.get_children()[:-2]))
        for i in helpcontent.help:
            self.add_section(i[0])
            for text, icon in i[1:]:
                self.add_paragraph(text, icon)

    def add_section(self, section_text):
        hbox = gtk.HBox()
        label = gtk.Label()
        label.set_use_markup(True)
        label.set_markup('<b>%s</b>' % section_text)
        label.set_line_wrap(True)
        label.set_size_request(self._max_text_width, -1)
        hbox.add(label)
        hbox.show_all()
        self._vbox.pack_start(hbox, False, False, padding=5)

    def add_paragraph(self, text, icon=None):
        hbox = gtk.HBox()
        label = gtk.Label(text)
        label.set_justify(gtk.JUSTIFY_LEFT)
        label.set_line_wrap(True)
        hbox.add(label)
        if icon is not None:
            _icon = Icon(icon_name=icon)
            hbox.add(_icon)
            label.set_size_request(self._max_text_width - 20, -1)
        else:
            label.set_size_request(self._max_text_width, -1)

        hbox.show_all()
        self._vbox.pack_start(hbox, False, False, padding=5)
