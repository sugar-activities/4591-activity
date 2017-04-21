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
logger = logging.getLogger('canvas')
import json

import gtk
from math import *

from sweetener import profile
from sweetener.colors import color2string

import expressions
from graph import Graph
from graph import SCALE_TYPE_DEC
from graph import SCALE_TYPE_RAD
from graph import SCALE_TYPE_CUST
from functions import FunctionsList

x_res = 1
x_max = '5.0'
x_min = '-5.0'
x_scale = '1.0'
y_max = '3.0'
y_min = '-3.0'
y_scale = '1.0'


class Canvas(gtk.HPaned):
    #def write_file(self, file_path):
        #x, y, w, h = self.graph.get_allocation()
        #pix_buffer = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, w, h)
        #pix_buffer.get_from_drawable(self.graph.pix_map,
                                     #self.graph.pix_map.get_colormap(),
                                     #0, 0, 0, 0, w, h)
        #pix_buffer.save(file_path, 'png')

    def write_file(self, path):
        jfile = open(path, 'w')

        _list = []
        for i in self.functions_list.get_list():
            _list.append([color2string(i[0]), i[2]])

        graph_props = {'list': _list,
                      'xmin': self.graph.xmin,
                      'xmax': self.graph.xmax,
                      'ymin': self.graph.ymin,
                      'ymax': self.graph.ymax}

        try:
            json.dump(graph_props, jfile)
        finally:
            jfile.close()

    def read_file(self, path):
        jfile = open(path, 'r')
        try:
            self.starting_program = False
            graph_props = json.load(jfile)
            self.functions_list.model.clear()
            for i in graph_props['list']:
                self.functions_list.append_function(gtk.gdk.color_parse(i[0]),
                                                    i[1])
                self.update_graph(None, self.functions_list.get_list())
        except Exception, err:
            logger.error(str(err))
        finally:
            jfile.close()

    def __init__(self, toolbar_box, activity):
        gtk.HPaned.__init__(self)
        self.activity = activity
        self.x_max = x_max
        self.x_min = x_min
        self.x_scale = x_scale
        self.y_max = y_max
        self.y_min = y_min
        self.y_scale = y_scale
        self.w = 0
        self.h = 0
        self._resize_queue = 4
        self._resize_constant = 4
        self.graph = Graph()
        self.activity.connect('key-press-event',
                                self.graph._key_press_event)
        self.activity.connect('key-release-event',
                                self.graph._key_release_event)
        self.graph.connect('update-x-y', self._update_coordinates)
        self.starting_program = True
        self.graph.connect('repopulate-parameter-entries',
                           self.parameter_entries_repopulate)
        self.toolbar_box = toolbar_box
        self.exports = {'image/x-generic': self.graph.save_png}
        self.toolbar_box.connect('append-function', self._append_function)
        self.toolbar_box.connect('remove-function', self._remove_function)
        self.toolbar_box.connect('color-updated', self._update_line_color)
        self.toolbar_box.connect('evaluate', self._evaluate_cb)
        # FIXME: Have to connect correctly all the motions in toolbar
        self.toolbar_box.connect('motion_notify_event', self._event_motion)
        self.toolbar_box.view.connect('zoom-in', self.zoom_in)
        self.toolbar_box.view.connect('zoom-out', self.zoom_out)
        self.toolbar_box.view.connect('zoom-reset', self.zoom_reset)
        self.toolbar_box.view.connect('scale-range',
                                              self.update_parameters)
        self.toolbar_box.view.connect('fullscreen', self._fullscreen)
        self.toolbar_box.view.connect('connect-points',
                                              self.connect_points)
        self.toolbar_box.view.connect('decimal-scale',
                                                  self.scale_dec)
        self.toolbar_box.view.connect('radian-scale',
                                                  self.scale_rad)
        self.toolbar_box.view.connect('custom-scale',
                                                  self.scale_cust)
        self.toolbar_box.view.connect('scale', self._update_scale)
        self.toolbar_box.view.connect('show-grid',
                                lambda w, d: self.graph.set_show_grid(d))
        #self.toolbar_box.show()
        self.functions_list = FunctionsList()
        self.functions_list.connect('motion_notify_event', self._event_motion)
        self.functions_list.connect('list-updated',
                                    self.update_graph)
        self.functions_list.connect('function-selected',
                                    self._update_color_selection)
        self.functions_list.show()
        functions_box = gtk.VBox()
        function_entry = gtk.Entry()
        function_entry.show()
        function_entry.connect('activate', self._new_function_cb)
        functions_box.pack_start(function_entry, False, True, 0)
        functions_window = gtk.ScrolledWindow()
        functions_window.add(self.functions_list)
        functions_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        functions_window.set_hadjustment(self.functions_list.get_hadjustment())
        functions_window.set_vadjustment(self.functions_list.get_vadjustment())
        functions_window.show()
        functions_box.pack_start(functions_window, True, True, 0)
        hbox = gtk.HBox()
        self.xlabel = gtk.Label()
        self.xlabel.set_alignment(0.5, 0.5)
        self.xlabel.show()
        hbox.pack_start(self.xlabel, True, True, 0)
        self.ylabel = gtk.Label()
        self.ylabel.set_alignment(0.5, 0.5)
        self.ylabel.show()
        hbox.pack_start(self.ylabel, True, True, 0)
        hbox.show()
        functions_box.pack_start(hbox, False, True, 0)
        self.pack1(functions_box)
        functions_box.show_all()
        self.toolbar_box.view.x_min_entry.set_text(self.x_min)
        self.toolbar_box.view.x_max_entry.set_text(self.x_max)
        self.toolbar_box.view.x_scale_entry.set_text(self.x_scale)
        self.toolbar_box.view.y_min_entry.set_text(self.y_min)
        self.toolbar_box.view.y_max_entry.set_text(self.y_max)
        self.toolbar_box.view.y_scale_entry.set_text(self.y_scale)
        self.pack2(self.graph)
        self.graph.show()
        self.connect('expose-event', self._paned_expose_event_cb)

    def new(self):
        self.functions_list.model.clear()
        self._append_function(None)

    def _event_motion(self, widget, event):
        self.graph.pointer = None
        self.graph.queue_draw()
        self.xlabel.set_text('')
        self.ylabel.set_text('')

    def _update_coordinates(self, widget, x, y):
        self.xlabel.set_text("x = " + str(int(x * 100) / 100.0))
        self.ylabel.set_text("y = " + str(int(y * 100) / 100.0))

    def _fullscreen(self, widget):
        self.previous_size = self._resize_constant
        self._resize_queue = 0
        self.activity.fullscreen()

    def _new_function_cb(self, widget):
        text = widget.get_text()
        if len(self.functions_list.get_list()) % 2 == 0:
            color = profile.get_fill_color(self)
        else:
            color = profile.get_stroke_color(self)
        self.functions_list.append_function(color, text)
        self.update_graph(None, self.functions_list.get_list())
        widget.set_text('')
        number = len(self.functions_list.get_list())
        if number == 1:
            self.toolbar_box.remove_function.sensitive = False
        else:
            self.toolbar_box.remove_function.sensitive = True

    def _update_scale(self, widget=None):
        xscale, yscale = self.toolbar_box.view.get_scale()
        self.graph.set_x_scale(xscale)
        self.graph.set_y_scale(yscale)
        self.update_graph(None, self.functions_list.get_list())

    def _evaluate_cb(self, widget, x):
        safe_dict = self.graph.safe_dict
        try:
            x = eval(expressions.convert(x), {'__builtins__': {}}, safe_dict)
            safe_dict['x'] = x
        except:
            safe_dict['x'] = None
        self.functions_list.evaluate(safe_dict)

    def update_parameters(self, widget):
        xmin, xmax, ymin, ymax = self.toolbar_box.view.get_scale_range()
        self.graph.set_xmin(xmin)
        self.graph.set_xmax(xmax)
        self.graph.set_ymin(ymin)
        self.graph.set_ymax(ymax)
        self.update_graph(None, self.functions_list.get_list())

    def _paned_expose_event_cb(self, widget, event):
        #logger.debug('Paned expose')
        x, y, w, h = self.get_allocation()
        if self._resize_queue == None:
            if self.w != w or self.h != h:
                self._resize_queue = self._resize_constant
        self.w = w
        self.h = h
        min_position = self.get_property('min-position')
        max_position = self.get_property('max-position')    
        if self._resize_queue != None:
            #logger.debug('Resize a %f percent from %s %s' %
            #            (self._resize_queue * 10, min_position, max_position))
            if self._resize_queue == 0:
            #    logger.debug('Resize to %d' % min_position)
                self.set_position(min_position)
            else:
                pos = (max_position - min_position) /\
                                        self._resize_queue + min_position
                self.set_position(int(pos))
            #    logger.debug('Resize to %d' % pos)
            self._resize_queue = None
        position = self.get_position()
        self._resize_constant = float(max_position - min_position) / position if position != 0 else 0

    def parameter_entries_repopulate(self, widget=None):
        # set text in entries for parameters
        self.toolbar_box.view.x_min_entry.set_text(
                                                         str(self.graph.xmin))
        self.toolbar_box.view.x_max_entry.set_text(
                                                         str(self.graph.xmax))
        self.toolbar_box.view.x_scale_entry.set_text(
                                                       str(self.graph.x_scale))
        self.toolbar_box.view.y_min_entry.set_text(
                                                         str(self.graph.ymin))
        self.toolbar_box.view.y_max_entry.set_text(
                                                         str(self.graph.ymax))
        self.toolbar_box.view.y_scale_entry.set_text(
                                                       str(self.graph.y_scale))

    def zoom_in(self, widget, event=None):
        'Narrow the plotted section by half'
        center_x = (self.graph.xmin + self.graph.xmax) / 2
        center_y = (self.graph.ymin + self.graph.ymax) / 2
        range_x = (self.graph.xmax - self.graph.xmin)
        range_y = (self.graph.ymax - self.graph.ymin)

        self.graph.xmin = center_x - (range_x / 4)
        self.graph.xmax = center_x + (range_x / 4)
        self.graph.ymin = center_y - (range_y / 4)
        self.graph.ymax = center_y + (range_y / 4)

        self.parameter_entries_repopulate()
        self.update_graph(None, self.functions_list.get_list())

    def zoom_out(self, widget, event=None):
        """Double the plotted section"""
        center_x = (self.graph.xmin + self.graph.xmax) / 2
        center_y = (self.graph.ymin + self.graph.ymax) / 2
        range_x = (self.graph.xmax - self.graph.xmin)
        range_y = (self.graph.ymax - self.graph.ymin)

        self.graph.xmin = center_x - (range_x)
        self.graph.xmax = center_x + (range_x)
        self.graph.ymin = center_y - (range_y)
        self.graph.ymax = center_y + (range_y)

        self.parameter_entries_repopulate()
        self.update_graph(None, self.functions_list.get_list())

    def zoom_reset(self, widget, event=None):
        """Set the range back to the user's input"""

        self.graph.xmin = -5.0
        self.graph.ymin = -3.0
        self.graph.xmax = 5.0
        self.graph.ymax = 3.0
        self.toolbar_box.view.x_min_entry.set_text(self.x_min)
        self.toolbar_box.view.x_max_entry.set_text(self.x_max)
        self.toolbar_box.view.x_scale_entry.set_text(self.x_scale)
        self.toolbar_box.view.y_min_entry.set_text(self.y_min)
        self.toolbar_box.view.y_max_entry.set_text(self.y_max)
        self.toolbar_box.view.y_scale_entry.set_text(self.y_scale)
        self.update_graph(None, self.functions_list.get_list())

    def scale_dec(self, widget):
        self.graph.scale_style = SCALE_TYPE_DEC
        self.update_graph(None, self.functions_list.get_list())

    def scale_rad(self, widget):
        self.graph.scale_style = SCALE_TYPE_RAD
        self.update_graph(None, self.functions_list.get_list())

    def scale_cust(self, widget):
        self.graph.scale_style = SCALE_TYPE_CUST
        self.update_graph(None, self.functions_list.get_list())

    def connect_points(self, widget, connect_points):
        self.graph.connect_points = connect_points
        self.update_graph(None, self.functions_list.get_list())

    def _update_line_color(self, widget, color):
        self.functions_list.set_current_line_color(color)
        self.update_graph(None, self.functions_list.get_list())

    def _update_color_selection(self, widget, color):
        self.toolbar_box.color_item.set_color(color)
        self.update_graph(None, self.functions_list.get_list())

    def _remove_function(self, widget):
        self.functions_list.remove_function()
        self.update_graph(None, self.functions_list.get_list())
        return len(self.functions_list.get_list())

    def _append_function(self, widget):
        if len(self.functions_list.get_list()) % 2 == 0:
            color = profile.get_fill_color(self)
        else:
            color = profile.get_stroke_color(self)
        self.functions_list.append_function(color)
        self.update_graph(None, self.functions_list.get_list())
        return len(self.functions_list.get_list())

    def update_graph(self, widget, info):
#        self._evaluate_cb(None, self.toolbar_box.evaluate_entry.get_text())
        self.graph.reload_functions([(func,
                                      color,
                                      selected) for color,
                                                 name,
                                                 func,
                                                 selected in info])
