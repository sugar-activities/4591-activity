"""
This is a Gtk TreeView to list and modify the plotted functions
"""
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
logger = logging.getLogger('functions')
import gobject
import gtk

from sweetener.colors import color2string
from sweetener.colors import XoColor
from sweetener.icon import CellRendererIcon

import expressions


class FunctionsList(gtk.TreeView):
    __gsignals__ = {'list-updated': (gobject.SIGNAL_RUN_LAST,
                                     gobject.TYPE_NONE,
                                     (gobject.TYPE_PYOBJECT,)),
                    'function-selected': (gobject.SIGNAL_RUN_LAST,
                                          gobject.TYPE_NONE,
                                          (gobject.TYPE_PYOBJECT,))}

    def __init__(self):
        gtk.TreeView.__init__(self)
        self.set_rules_hint(True)
        self.grab_focus()
        self.model = gtk.ListStore(object, str, str, str, bool)
        self.set_model(self.model)
        column = gtk.TreeViewColumn()
        color_renderer = CellRendererIcon(self)
        width, height = gtk.icon_size_lookup(gtk.ICON_SIZE_SMALL_TOOLBAR)
        color_renderer.set_fixed_size(int(width * 1.5), int(height * 1.5))
        # int(style.SMALL_ICON_SIZE * 4), -1)
        color_renderer.set_size(int(height * 1.5))
        color_renderer.set_icon_name('color-preview')
        color_renderer.props.stroke_color = '#000000'
        color_renderer.props.fill_color = '#FFFFFF'
        color_renderer.props.prelit_stroke_color = "#666666"
        color_renderer.props.prelit_fill_color = "#FFFFFF"
        column.pack_start(color_renderer, False)
        column.add_attribute(color_renderer, 'xo-color', 0)
        name_renderer = gtk.CellRendererText()
        column.pack_start(name_renderer, False)
        column.add_attribute(name_renderer, 'text', 1)
        text_renderer = gtk.CellRendererText()
        text_renderer.set_property('editable', True)
        text_renderer.connect('edited', self._function_changed)
        column.pack_start(text_renderer, True)
        column.add_attribute(text_renderer, 'text', 2)
        self.set_headers_visible(False)
        self.append_column(column)
        self.evaluating_column = gtk.TreeViewColumn()
        y_renderer = gtk.CellRendererText()
        y_renderer.set_property('text', ' = ')
        self.evaluating_column.pack_start(y_renderer, False)
        evaluation_cell = gtk.CellRendererText()
        self.evaluating_column.pack_start(evaluation_cell, False)
        self.evaluating_column.add_attribute(evaluation_cell, 'text', 3)
        self.append_column(self.evaluating_column)
        self.evaluating_column.set_visible(False)
        self.selection = self.get_selection()
        self.selection.set_select_function(self.update_color)
        self.updating_color = False

    def evaluate(self, safe_dict):
        for func in self.model:
            if safe_dict['x'] is None:
                self.evaluating_column.set_visible(False)
                return
            result = eval(expressions.convert(func[2]),
                          {'__builtins__': {}}, safe_dict)
            func[3] = str(result)
        self.evaluating_column.set_visible(True)

    def set_current_line_color(self, color):
        if not self.updating_color:
            rows = self.selection.get_selected_rows()
            self.model[rows[1][0]][0] = XoColor(color + "," + color)

    def update_color(self, info):
        path = info[0]
        for i in self.model:
            i[-1] = False
        color = self.model[path][0]
        self.updating_color = True
        self.model[path][-1] = True
        self.emit('function-selected', color.get_fill_color())
        self.updating_color = False
        return True

    def get_list(self):
        funcs = []
        for func in self.model:
            row = [gtk.gdk.color_parse(func[0].get_fill_color()),
                    func[1], func[2], func[-1]]
            funcs.append(row)
#        logger.debug(str(funcs))
        return funcs

    def _function_changed(self, widget, path, new_text):
        self.model[path][2] = new_text
        for i in self.model:
            i[-1] = False
        self.model[path][-1] = True
        self.emit('list-updated', self.get_list())

    def append_function(self, color, expression='sin(x)'):
        self.selection.select_iter(self.model.append([
                   XoColor(color2string(color) + "," + color2string(color)),
                 "f%d(x) = " % (len(self.model) + 1), expression, None, True]))

    def remove_function(self):
        rows = self.selection.get_selected_rows()
        if len(rows) >= 2 and len(rows[1]) >= 1:
            _iter = self.model.get_iter(rows[1][0])
            self.model.remove(_iter)
        count = 0
        for i in self.model:
            count += 1
            i[1] = 'f%d(x) =' % count
            _iter = self.model.get_iter(count - 1)
            self.selection.select_iter(_iter)
