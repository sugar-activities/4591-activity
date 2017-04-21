#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012 S. Daniel Francis <francis@sugarlabs.org>
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
logger = logging.getLogger('options')

from gettext import gettext as _
import gobject
import gtk

from sweetener import stock
from sweetener.itembox import ItemBox
from sweetener.basic_options import BasicOptions
from sweetener.itemgroup import ItemGroup
from sweetener.itemgroup import SubGroup
from sweetener.itemgroup import GhostGroup
from sweetener.item import Item
from sweetener.toggleitem import ToggleItem
from sweetener.radioitem import RadioItem
from sweetener.settingsitem import SettingsItem
from sweetener.shortcontentitem import ShortContentItem
from sweetener.settingsradioitem import SettingsRadioItem
from sweetener.coloritem import ColorItem
from sweetener.help import Help

#from helpbutton import HelpButton


class ViewOptions(ItemGroup):
    __gsignals__ = {'zoom-in': (gobject.SIGNAL_RUN_FIRST,
                                gobject.TYPE_NONE,
                                tuple()),
                    'zoom-out': (gobject.SIGNAL_RUN_FIRST,
                                gobject.TYPE_NONE,
                                tuple()),
                    'zoom-reset': (gobject.SIGNAL_RUN_FIRST,
                                   gobject.TYPE_NONE,
                                   tuple()),
                    'scale-range': (gobject.SIGNAL_RUN_FIRST,
                                    gobject.TYPE_NONE,
                                    tuple()),
                    'fullscreen': (gobject.SIGNAL_RUN_FIRST,
                                   gobject.TYPE_NONE,
                                   tuple()),
                    'connect-points': (gobject.SIGNAL_RUN_FIRST,
                                       gobject.TYPE_NONE,
                                       (gobject.TYPE_BOOLEAN,)),
                    'decimal-scale': (gobject.SIGNAL_RUN_FIRST,
                                      gobject.TYPE_NONE,
                                      tuple()),
                    'radian-scale': (gobject.SIGNAL_RUN_FIRST,
                                     gobject.TYPE_NONE,
                                     tuple()),
                    'custom-scale': (gobject.SIGNAL_RUN_FIRST,
                                     gobject.TYPE_NONE,
                                     tuple()),
                    'scale': (gobject.SIGNAL_RUN_FIRST,
                              gobject.TYPE_NONE,
                              tuple()),
                    'show-grid': (gobject.SIGNAL_RUN_LAST,
                                  gobject.TYPE_NONE,
                                  (gobject.TYPE_BOOLEAN,))}

    def __init__(self, box):
        ItemGroup.__init__(self, box, _('_View'), 'toolbar-view')
        #gtk.stock_add(('show-grid', 'Show grid', ))
        self.setup_scale_style()
        stock.register('graph-plotter-show-grid',
                        _('Show _grid'), '<Ctrl>G', 'insert-table')
        show_grid = ToggleItem(True, 'graph-plotter-show-grid')
        show_grid.connect('toggled',
                          lambda w, active: self.emit('show-grid', active))
        self.append_item(show_grid)
        stock.register('graph-plotter-connect-points', _('Connect _points'),
                        '<Ctrl>I', 'connect-points')
        connect_points_option = ToggleItem(True,
                                           'graph-plotter-connect-points')
        connect_points_option.connect('toggled',
                        lambda w, active: self.emit('connect-points', active))
        self.append_item(connect_points_option)
        self.append_separator()
        self.setup_zoom()
        self.append_separator()
        fullscreen_option = Item(gtk.STOCK_FULLSCREEN)
        fullscreen_option.connect('activate',
                                  lambda w: self.emit('fullscreen'))
        self.append_item(fullscreen_option)
        #elambda w: self.emit('fullscreen'), gtk.STOCK_FULLSCREEN)
        #fullscreen_button = ToolButton('view-fullscreen')
        #fullscreen_button.props.tooltip = _('Fullscreen')
        #fullscreen_button.props.accelerator = '<Alt>Return'
        #fullscreen_button.connect('clicked',
        #                          lambda w: self.emit('fullscreen'))
        #fullscreen_button.show()
        #self.toolbar.insert(fullscreen_button, -1)

    def setup_zoom(self):
        zoom_in_item = Item(gtk.STOCK_ZOOM_IN)
        zoom_in_item.connect('activate', lambda w: self.emit('zoom-in'))
        self.append_item(zoom_in_item)
        zoom_out_item = Item(gtk.STOCK_ZOOM_OUT)
        zoom_out_item.connect('activate', lambda w: self.emit('zoom-out'))
        self.append_item(zoom_out_item)
        zoom_reset_item = Item(gtk.STOCK_ZOOM_100)
        zoom_reset_item.connect('activate', lambda w: self.emit('zoom-reset'))
        self.append_item(zoom_reset_item)

    def setup_scale_range(self, subgroup):
        stock.register('graph-plotter-scale-range', _('R_ange'),
                        '<Ctrl>N', 'cell-size')
        self.scale_range = SettingsItem(self.activity,
                                        'graph-plotter-scale-range', True)
        self.scale_range.tooltip = _('Scale range')
        self.scale_range.connect('closed', lambda w: self.emit('scale-range'))

        scale_range_table = gtk.Table(4, 2, False)
        x_min_label = gtk.Label(_('X min') + ' =')
        x_min_label.set_justify(gtk.JUSTIFY_RIGHT)
        self.x_min_entry = gtk.Entry()
        self.x_min_entry.set_size_request(90, -1)
        self.x_min_entry.set_alignment(0)
        self.x_min_entry.connect('activate',
                                 lambda w: self.emit('scale-range'))
        scale_range_table.attach(x_min_label, 0, 1, 0, 1, xpadding=5)
        scale_range_table.attach(self.x_min_entry, 1, 2, 0, 1)
        x_max_label = gtk.Label(_('X max') + ' =')
        x_max_label.set_justify(gtk.JUSTIFY_RIGHT)
        self.x_max_entry = gtk.Entry()
        self.x_max_entry.set_size_request(90, -1)
        self.x_max_entry.set_alignment(0)
        self.x_max_entry.connect('activate',
                                 lambda w: self.emit('scale-range'))
        scale_range_table.attach(x_max_label, 0, 1, 2, 3, xpadding=5)
        scale_range_table.attach(self.x_max_entry, 1, 2, 2, 3)

        y_min_label = gtk.Label(_('Y min') + ' =')
        y_min_label.set_justify(gtk.JUSTIFY_RIGHT)
        self.y_min_entry = gtk.Entry()
        self.y_min_entry.set_size_request(90, -1)
        self.y_min_entry.set_alignment(0)
        self.y_min_entry.connect('activate',
                                 lambda w: self.emit('scale-range'))
        scale_range_table.attach(y_min_label, 2, 3, 0, 1, xpadding=5)
        scale_range_table.attach(self.y_min_entry, 3, 4, 0, 1)
        y_max_label = gtk.Label(_('Y max') + ' =')
        y_max_label.set_justify(gtk.JUSTIFY_RIGHT)
        self.y_max_entry = gtk.Entry()
        self.y_max_entry.set_size_request(90, -1)
        self.y_max_entry.set_alignment(0)
        self.y_max_entry.connect('activate',
                                 lambda w: self.emit('scale-range'))
        scale_range_table.attach(y_max_label, 2, 3, 2, 3, xpadding=5)
        scale_range_table.attach(self.y_max_entry, 3, 4, 2, 3)
        scale_range_table.show_all()
        self.scale_range.content = scale_range_table
        subgroup.append_item(self.scale_range)
        subgroup.append_separator(False)

    def get_scale_range(self):
        return [self.x_min_entry.get_text(),
                self.x_max_entry.get_text(),
                self.y_min_entry.get_text(),
                self.y_max_entry.get_text()]

    def get_scale(self):
        return self.x_scale_entry.get_text(), self.y_scale_entry.get_text()

    def setup_scale_style(self):
        subgroup = SubGroup(self, _('_Scale'))
        self.setup_scale_range(subgroup)
        stock.register('graph-plotter-decimal', _('_Decimal'),
                        '<Ctrl>D', 'decimal')
        self.decimal_option = RadioItem(None, stock_id='graph-plotter-decimal')
        self.decimal_option.tooltip = _('Decimal scale')
        self.decimal_option.connect('toggled',
                                    lambda w, a: self.emit('decimal-scale'))
        subgroup.append_item(self.decimal_option)
        stock.register('graph-plotter-radians', _('_Radian'), '<Ctrl>I',
                        'radian')
        self.radians_option = RadioItem(self.decimal_option, False,
                                        'graph-plotter-radians')
        self.radians_option.tooltip = _('Radian scale')
        self.radians_option.connect('toggled',
                                    lambda w, a: self.emit('radian-scale'))
        subgroup.append_item(self.radians_option)
        stock.register('graph-plotter-custom', _('_Custom'), '<Ctrl>T',
                        'custom')
        self.custom_option = SettingsRadioItem(self.decimal_option, False,
                                               self.activity,
                                               'graph-plotter-custom')
        self.custom_option.set_stock_id('graph-plotter-custom')
        self.custom_option.tooltip = _('Custom scale')
        self.custom_option.connect('toggled',
                                    lambda w, a: self.emit('custom-scale'))
        self.custom_option.connect('closed', lambda w: self.emit('scale'))
        self.custom_option.content = self.setup_scale_palette()
        subgroup.append_item(self.custom_option)
#        custom_item = RadioToolButton()
#        custom_item.set_named_icon('custom')
#        custom_item.set_tooltip(_('Custom scale'))
#        custom_item.props.accelerator = '<Ctrl><Shift>C'
#        custom_item.set_group(radians_item)
#        custom_item.connect('toggled',
#                            lambda w: self.emit('custom-scale'))
#        custom_item.show()
#        scale_palette = custom_item.get_palette()
#        self.setup_scale_palette(scale_palette)
#        self.toolbar.insert(custom_item, -1)

    def setup_scale_palette(self):
        scale_table = gtk.Table(2, 2, False)
        self.x_scale_entry = gtk.Entry()
        self.x_scale_entry.connect('activate',
                                   lambda w: self.emit('scale'))
        self.x_scale_entry.set_size_request(90, -1)
        self.y_scale_entry = gtk.Entry()
        self.y_scale_entry.connect('activate',
                                    lambda w: self.emit('scale'))
        self.y_scale_entry.set_size_request(90, -1)
        x_scale_label = gtk.Label(_('X scale'))
        x_scale_label.set_alignment(0, .5)
        y_scale_label = gtk.Label(_('Y scale'))
        y_scale_label.set_alignment(0, .5)
        scale_table.attach(x_scale_label, 0, 1, 0, 1, xpadding=5)
        scale_table.attach(self.x_scale_entry, 1, 2, 0, 1)
        scale_table.attach(y_scale_label, 0, 1, 1, 2, xpadding=5)
        scale_table.attach(self.y_scale_entry, 1, 2, 1, 2)
        scale_table.show_all()
        return scale_table


class Options(ItemBox):
    __gsignals__ = {'append-function': (gobject.SIGNAL_RUN_LAST,
                                        gobject.TYPE_INT,
                                        tuple()),
                    'remove-function': (gobject.SIGNAL_RUN_LAST,
                                        gobject.TYPE_INT,
                                        tuple()),
                    'color-updated': (gobject.SIGNAL_RUN_FIRST,
                                      gobject.TYPE_NONE,
                                      (gobject.TYPE_PYOBJECT,)),
                    'evaluate': (gobject.SIGNAL_RUN_FIRST,
                                 gobject.TYPE_NONE,
                                 (gobject.TYPE_STRING,)),
                    'save-png': (gobject.SIGNAL_RUN_FIRST,
                                 gobject.TYPE_NONE,
                                 (gobject.TYPE_STRING,))}

    def __init__(self, activity):
        ItemBox.__init__(self, activity)
        self.activity = activity
        self.basic = BasicOptions(activity, self,
                                  [(_('_image'),
                                    'image/x-generic',
                                    'image/*',
                                    _('Images'))])
        #activity_button.page.share.hide()
        self.view = ViewOptions(self)
        self.ghost = GhostGroup(self, _('F_unction'))
        add_function = Item(gtk.STOCK_ADD, True)
        add_function.tooltip = _('Append a new function')
        add_function.connect('activate',
                             self._append_function_cb)
        self.ghost.append_item(add_function)
        self.remove_function = Item(gtk.STOCK_REMOVE, True)
        self.remove_function.tooltip = _('Remove the selected function')
        self.remove_function.connect('activate',
                                     self._remove_function_cb)
        self.ghost.append_item(self.remove_function)
        self.remove_function.sensitive = False
        self.color_item = ColorItem(activity, True)
        self.color_item.tooltip = _('Plot color')
        self.color_item.connect('updated',
                                lambda w, color: self.emit('color-updated',
                                                           color))
        self.ghost.append_item(self.color_item)

#        self.setup_help_button()
#        separator = gtk.SeparatorToolItem()
#        separator.show()
#        separator.set_expand(True)
#        separator.set_draw(False)
#        self.toolbar.insert(separator, -1)
        evaluate_label = gtk.Label('x = ')
        evaluate_label.show()
        self.evaluate_entry = gtk.Entry()
        self.evaluate_entry.set_size_request(150, -1)
        self.evaluate_entry.connect('changed',
                                    lambda w: self.emit('evaluate',
                                                           w.get_text()))
        self.evaluate_entry.show()
        hbox = gtk.HBox()
        hbox.pack_start(evaluate_label, False, False, 0)
        hbox.pack_start(self.evaluate_entry, True, True, 0)
        hbox.show()
        evaluate_entry_item = ShortContentItem(activity,
                                               'graph-plotter-evaluate', True)
        evaluate_entry_item.separator = self.ghost.append_separator(True)
        stock.register('graph-plotter-evaluate', _('_Evaluate'),
                       '<Ctrl>E', None)
        evaluate_entry_item.set_stock_id('graph-plotter-evaluate')
        evaluate_entry_item.content = hbox
        self.ghost.append_item(evaluate_entry_item)
        self.help = Help(self)

    def _append_function_cb(self, widget):
        number = self.emit('append-function')
        logger.debug(number)
        if number == 1:
            self.remove_function.sensitive = False
        else:
            self.remove_function.sensitive = True

    def _remove_function_cb(self, widget):
        number = self.emit('remove-function')
        logger.debug(number)
        if number == 1:
            self.remove_function.sensitive = False
        else:
            self.remove_function.sensitive = True
