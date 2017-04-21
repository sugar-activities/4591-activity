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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

#import sys
import logging
logger = logging.getLogger('graph')

from math import *
fac = lambda n: [1, 0][n > 0] or fac(n - 1) * n
from numpy import sinc

import gobject
import gtk
import pango
import cairo

import expressions

SCALE_TYPE_DEC = 0
SCALE_TYPE_RAD = 1
SCALE_TYPE_CUST = 2


def sub_dict(somedict, somekeys, default=None):
    return dict([(k, somedict.get(k, default)) for k in somekeys])


def marks(min_val, max_val, minor=1):
    '''yield positions of scale marks between min and max.
    For making minor marks,
        set minor to the number of minors you want between majors'''
    try:
        min_val = float(min_val)
        max_val = float(max_val)
    except:
        print 'needs 2 numbers'
        raise ValueError

    if(min_val >= max_val):
        print 'min bigger or equal to max'
        raise ValueError

    a = 0.2  # tweakable control for when to switch scales
            # big a value results in more marks

    a = a + log10(minor)

    width = max_val - min_val
    log10_range = log10(width)

    interval = 10 ** int(floor(log10_range - a))
    lower_mark = min_val - fmod(min_val, interval)

    if lower_mark < min_val:
        lower_mark += interval

    a_mark = lower_mark
    while a_mark <= max_val:
        if abs(a_mark) < interval / 2:
            a_mark = 0
        yield a_mark
        a_mark += interval


class Graph(gtk.DrawingArea):
    __gsignals__ = {'repopulate-parameter-entries': (gobject.SIGNAL_RUN_LAST,
                                                     gobject.TYPE_NONE,
                                                     tuple()),
                    'update-x-y': (gobject.SIGNAL_RUN_LAST,
                                   gobject.TYPE_NONE,
                                   (gobject.TYPE_FLOAT,
                                    gobject.TYPE_FLOAT))}

    safe_dict = safe_list = {'acos': acos,
                             'asin': asin,
                             'atan': atan,
                             'atan2': atan2,
                             'ceil': ceil,
                             'cos': cos,
                             'cosh': cosh,
                             'degrees': degrees,
                             'e': e,
                             'exp': exp,
                             'fabs': fabs,
                             'floor': floor,
                             'fmod': fmod,
                             'frexp': frexp,
                             'hypot': hypot,
                             'ldexp': ldexp,
                             'log': log,
                             'log10': log10,
                             'modf': modf,
                             'pi': pi,
                             'pow': pow,
                             'radians': radians,
                             'sin': sin,
                             'sinh': sinh,
                             'sqrt': sqrt,
                             'tan': tan,
                             'tanh': tanh,
                             'fac': fac,
                             'sinc': sinc}
    x_res = 1
    x_max = '5.0'
    x_min = '-5.0'
    x_scale = '1.0'
    y_max = '3.0'
    y_min = '-3.0'
    y_scale = '1.0'

    xmax = 5.0
    xmin = -5.0
    xscale = 1.0
    ymax = 3.0
    ymin = -3.0
    yscale = 1.0
    _show_grid = True
    shift = False
    _move_from = None

    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.connect_points = True
        #add any needed builtins back in.
        self.safe_dict['abs'] = abs
        #logger.debug(str(self.safe_dict))
        self.pointer = None

        self.functions = []
        self.new_x = 0
        self.y = None
        self.prev_y = [None, None, None]
        self.selection = [[None, None], [None, None]]
        self.set_events(gtk.gdk.ALL_EVENTS_MASK)
        self.scale_style = SCALE_TYPE_DEC
        self.follow_function = False
#        self.set_flags(gtk.CAN_FOCUS)
#        self.add_events(gtk.gdk.BUTTON_PRESS_MASK)
#        self.add_events(gtk.gdk.KEY_PRESS)
#        self.grab_focus()
#        self.connect('key_press_event', self._key_press_event)
#        self.connect('key_release_event', self._key_relase_event)
        self.connect('expose_event', self._expose_event_cb)
        self.connect('configure_event', self._configure_event_cb)
        self.connect('button_press_event', self._button_press_event_cb)
        self.connect('button_release_event', self._button_release_event_cb)
        self.connect('motion_notify_event', self._motion_notify_event_cb)

    def save_png(self, path):
        thumb_surface = self.surface
        thumb_surface.write_to_png(path)

    def _key_press_event(self, widget, event):
        if event.keyval == 65505:  # keyval == Shift
            self.shift = True

        elif event.keyval == 65361 or event.keyval == 65430:  # Key Left
            scroll = 10 * float(self.xmax - self.xmin) / self.canvas_width
            self.xmin -= scroll
            self.xmax -= scroll
            self.queue_draw()

        elif event.keyval == 65362 or event.keyval == 65431:  # Key Up
            scroll = 10 * float(self.ymax - self.ymin) / self.canvas_height
            self.ymin += scroll
            self.ymax += scroll
            self.queue_draw()

        elif event.keyval == 65363 or event.keyval == 65432:  # Key Right
            scroll = 10 * float(self.xmax - self.xmin) / self.canvas_width
            self.xmin += scroll
            self.xmax += scroll
            self.queue_draw()

        elif event.keyval == 65364 or event.keyval == 65433:  # Key Down
            scroll = 10 * float(self.ymax - self.ymin) / self.canvas_height
            self.ymin -= scroll
            self.ymax -= scroll
            self.queue_draw()

    def _key_release_event(self, widget, event):
        if event.keyval == 65505:  # keyval == Shift
            self.shift = False
            self._move_from = None

    def set_show_grid(self, do):
        self._show_grid = do
        self.queue_draw()

    show_grid = property((lambda: _show_grid), set_show_grid)

    def reload_functions(self, functions):
        self.functions = functions
        self.queue_draw()

    def _button_press_event_cb(self, widget, event):
        if event.button == 1 and self.shift:
            self._move_from = [int(event.x), int(event.y)]
        elif event.button == 1:
            self.selection[0][0] = int(event.x)
            self.selection[0][1] = int(event.y)
            self.selection[1][0], self.selection[1][1] = None, None
            self.follow_function = not self.follow_function

    # End of selection
    def _button_release_event_cb(self, widget, event):
        if event.x != None and event.y != None\
                and self.selection[0][0] != None:
            if event.button == 1 and\
               event.x != self.selection[0][0] and\
               event.y != self.selection[0][1]:
                xmi = min(self.graph_x(self.selection[0][0]),
                                         self.graph_x(event.x))
                ymi = min(self.graph_y(self.selection[0][1]),
                                        self.graph_y(event.y))
                xma = max(self.graph_x(self.selection[0][0]),
                                       self.graph_x(event.x))
                yma = max(self.graph_y(self.selection[0][1]),
                                       self.graph_y(event.y))
                self.xmin, self.ymin, self.xmax, self.ymax = xmi, ymi, xma, yma
                self.follow_function = not self.follow_function
        self.selection = [[None, None], [None, None]]
        self._move_from = None
        self.queue_draw()
        self.y = None
        self.emit('repopulate-parameter-entries')

    # Draw rectangle during mouse movement
    def _motion_notify_event_cb(self, widget, event):
        x, y, state = self.get_window().get_pointer()
        self.pointer = [x, y]
        graph_x = self.graph_x(x)
        if self.scale_style == SCALE_TYPE_RAD:
            self.new_x = graph_x / pi
        else:
            self.new_x = graph_x
        if not self.follow_function or self.y == None:
            self.emit('update-x-y', self.new_x,  self.graph_y(y))
        if self.selection[0][0] != None:
            self.selection[1][0], self.selection[1][1] = int(x), int(y)
        elif self._move_from != None:
            xscroll = self._move_from[0] - x
            yscroll = self._move_from[1] - y
            self._move_from[0] = x
            self._move_from[1] = y
            self.xmin += xscroll * float(self.xmax - self.xmin) /\
                                                            self.canvas_width
            self.xmax += xscroll * float(self.xmax - self.xmin) /\
                                                            self.canvas_width
            self.ymin -= yscroll * float(self.ymax - self.ymin) /\
                                                            self.canvas_width
            self.ymax -= yscroll * float(self.ymax - self.ymin) /\
                                                            self.canvas_width
        self.queue_draw()

    def draw_cursor(self):
        if self.shift:
            if self._move_from != None:
                #logger.debug(str(self._move_from))
                self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.FLEUR))
            else:
                self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
        elif self.selection[0][0] != None:
            if self.selection[0][0] < self.selection[1][0]:
                if self.selection[0][1] < self.selection[1][1]:
                    self.get_window().set_cursor(
                                gtk.gdk.Cursor(gtk.gdk.BOTTOM_RIGHT_CORNER))
                else:
                    self.get_window().set_cursor(
                                   gtk.gdk.Cursor(gtk.gdk.TOP_RIGHT_CORNER))
            else:
                if self.selection[0][1] < self.selection[1][1]:
                    self.get_window().set_cursor(
                                    gtk.gdk.Cursor(gtk.gdk.BOTTOM_LEFT_CORNER))
                else:
                    self.get_window().set_cursor(
                                    gtk.gdk.Cursor(gtk.gdk.TOP_LEFT_CORNER))
        else:
            self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.CROSS))

    def draw_selection_rectangle(self):
        if self.selection[0][0] != None:
            #gc = self.drawing_area.get_style().black_gc
            #gc.set_function(gtk.gdk.INVERT)
            if self.selection[1][0] != None:
                x0 = min(self.selection[1][0], self.selection[0][0])
                y0 = min(self.selection[1][1], self.selection[0][1])
                w = abs(self.selection[1][0] - self.selection[0][0])
                h = abs(self.selection[1][1] - self.selection[0][1])
                self.context.rectangle(x0, y0, w, h)
                self.context.set_line_width(0.5)
                self.context.stroke()
                self.context.set_line_width(0.5)
                x0 = min(self.selection[0][0], int(self.selection[1][0]))
                y0 = min(self.selection[0][1], int(self.selection[1][1]))
                w = abs(int(self.selection[1][0]) - self.selection[0][0])
                h = abs(int(self.selection[1][1]) - self.selection[0][1])
                self.context.rectangle(x0, y0, w, h)
                self.context.stroke()
            self.context.set_line_width(2)
            return True
        else:
            return False

    def graph_x(self, x):
        'Calculate position on graph from point on canvas'
        return x * (self.xmax - self.xmin) / self.canvas_width + self.xmin

    def graph_y(self, y):
        return self.ymax - (y * (self.ymax - self.ymin) /\
                             self.canvas_height)

    def draw_queue(self):
        self.context.set_source_rgb(1, 1, 1)
        self.context.rectangle(0,
                               0,
                               self.canvas_width,
                               self.canvas_height)
        self.context.fill()
        self.context.set_source_rgb(0, 0, 0)
        #logger.debug('starter rectangle')
        if not self.draw_selection_rectangle():
            self.draw_pointer_reference()
            #logger.debug('pointer')
        self.draw_axis_and_grid()
        #logger.debug('axis and grid')
        self.plot_functions()
        #logger.debug('Plot functions')

    def draw_pointer_reference(self):
        if not self.shift:
            if self.pointer != None:
                x, y = self.pointer
                self.context.set_line_width(0.5)
                self.context.move_to(x, 0)
                self.context.line_to(x, self.canvas_height)
                if self.follow_function:
                    for i in self.functions:
                        if i[-1]:
                            expression = expressions.convert(i[0])
                            #logger.error(expression)
                            compiled = compile(expression, '', 'eval')
                            self.safe_dict['x'] = self.graph_x(x)
                            try:
                                y_g = eval(compiled, {'__builtins__': {}},
                                           self.safe_dict)
                                if self.new_x != None:
                                    self.emit('update-x-y', self.new_x, y_g)
                                y = int(round(self.canvas_y(y_g)))
                            except Exception, err:
                                #logging.error('graph: ' + str(err))
                                y = None
                if y != None:
                    self.context.move_to(0, y)
                    self.y = y
                    self.context.line_to(self.canvas_width, y)
                self.context.stroke()
            self.context.set_line_width(2)
            self.context.set_source_rgb(0, 0, 0)

    def draw_axis_and_grid(self):
        if (self.scale_style == SCALE_TYPE_CUST):
            #draw cross
            self.context.move_to(int(round(self.canvas_x(0))), 0)
            self.context.line_to(int(round(self.canvas_x(0))),
                                self.canvas_height)
            self.context.move_to(0, int(round(self.canvas_y(0))))
            self.context.line_to(self.canvas_width,
                                 int(round(self.canvas_y(0))))
            # old style axis marks
            # pixel interval between marks
            iv = self.xscale * self.canvas_width / (self.xmax - self.xmin)
            os = self.canvas_x(0) % iv  # pixel offset of first mark
            # loop over each mark.
            for i in xrange(int(self.canvas_width / iv + 1)):
                #multiples of iv,
                #cause adding of any error in iv, so keep iv as float
                # use round(),to get to closest pixel, int() to prevent warning
                self.context.move_to(int(round(os + i * iv)),
                                     int(round(self.canvas_y(0) - 5)))
                self.context.line_to(int(round(os + i * iv)),
                                     int(round(self.canvas_y(0) + 5)))
                self.context.stroke()
                if self._show_grid:
                    self.context.set_line_width(0.5)
                    self.context.set_dash((2, 2))
                    self.context.move_to(int(round(os + i * iv)),
                                         0)
                    self.context.line_to(int(round(os + i * iv)),
                                         self.canvas_height)
                    self.context.stroke()
                    self.context.set_source_rgb(0, 0, 0)
                    self.context.set_line_width(2)
                    self.context.set_dash((1, 0))

            # and the y-axis
            iv = self.yscale * self.canvas_height / (self.ymax - self.ymin)
            os = self.canvas_y(0) % iv
            for i in xrange(int(self.canvas_height / iv + 1)):
                self.context.move_to(int(round(self.canvas_x(0) - 5)),
                                     int(round(i * iv + os))),
                self.context.line_to(int(round(self.canvas_x(0) + 5)),
                                     int(round(i * iv + os)))
                self.context.stroke()
                if self._show_grid:
                    self.context.set_line_width(0.5)
                    self.context.set_dash((2, 2))
                    self.context.move_to(0, int(round(i * iv + os)))
                    self.context.line_to(self.canvas_width,
                                         int(round(i * iv + os)))
                    self.context.stroke()
                    self.context.set_source_rgb(0, 0, 0)
                    self.context.set_line_width(2)
                    self.context.set_dash((1, 0))
        else:
            #new style
            factor = 1
            if (self.scale_style == SCALE_TYPE_RAD):
                factor = pi

            # where to put the numbers
            numbers_x_pos = -10
            numbers_y_pos = 10

            # where to center the axis
            center_x_pix = int(round(self.canvas_x(0)))
            center_y_pix = int(round(self.canvas_y(0)))
            if (center_x_pix < 5):
                center_x_pix = 5
            if (center_x_pix < 20):
                numbers_x_pos = 10
            if (center_y_pix < 5):
                center_y_pix = 5
            if (center_x_pix > self.canvas_width - 5):
                center_x_pix = self.canvas_width - 5
            if (center_y_pix > self.canvas_height - 5):
                center_y_pix = self.canvas_height - 5
            if (center_y_pix > self.canvas_height - 20):
                numbers_y_pos = -10

            # draw cross
            self.context.move_to(center_x_pix, 0)
            self.context.line_to(center_x_pix, self.canvas_height)
            self.context.move_to(0, center_y_pix)
            self.context.line_to(self.canvas_width, center_y_pix)

            for i in marks(self.xmin / factor, self.xmax / factor):
                label = '%g' % i
                if (self.scale_style == SCALE_TYPE_RAD):
                    label += '\xCF\x80'
                i = i * factor

                self.context.move_to(int(round(self.canvas_x(i))),
                                     center_y_pix - 5),
                self.context.line_to(int(round(self.canvas_x(i))),
                                     center_y_pix + 5)

                self.layout.set_text(label)
                extents = self.layout.get_pixel_extents()[1]
                if (numbers_y_pos < 0):
                    adjust = extents[3]
                else:
                    adjust = 0
                self.context.move_to(int(round(self.canvas_x(i))),
                                     center_y_pix + numbers_y_pos - adjust)
                self.context.show_text(label)
                self.context.stroke()
                if self._show_grid:
                    self.context.set_line_width(0.5)
                    self.context.set_dash((2, 2))
                    self.context.move_to(int(round(self.canvas_x(i))), 0)
                    self.context.line_to(int(round(self.canvas_x(i))),
                                         self.canvas_height)
                    self.context.stroke()
                    self.context.set_line_width(2)
                    self.context.set_dash((1, 0))

            for i in marks(self.ymin, self.ymax):
                label = '%g' % i

                self.context.move_to(center_x_pix - 5,
                                     int(round(self.canvas_y(i))))
                self.context.line_to(center_x_pix + 5,
                                     int(round(self.canvas_y(i))))

                self.layout.set_text(label)
                extents = self.layout.get_pixel_extents()[1]
                if (numbers_x_pos < 0):
                    adjust = extents[2]
                else:
                    adjust = 0
                self.context.move_to(center_x_pix + numbers_x_pos - adjust,
                                         int(round(self.canvas_y(i))))
                self.context.show_text(label)
                self.context.stroke()
                if self._show_grid:
                    self.context.set_line_width(0.5)
                    self.context.set_dash((2, 2))
                    self.context.move_to(0, int(round(self.canvas_y(i))))
                    self.context.line_to(self.canvas_width,
                                         int(round(self.canvas_y(i))))
                    self.context.stroke()
                    self.context.set_line_width(2)
                    self.context.set_dash((1, 0))

            # minor marks
            for i in marks(self.xmin / factor, self.xmax / factor, minor=10):
                i = i * factor
                self.context.move_to(int(round(self.canvas_x(i))),
                                                    center_y_pix - 2)
                self.context.line_to(int(round(self.canvas_x(i))),
                                     center_y_pix + 2)

            for i in marks(self.ymin, self.ymax, minor=10):
                label = '%g' % i
                self.context.move_to(center_x_pix - 2,
                                     int(round(self.canvas_y(i))))
                self.context.line_to(center_x_pix + 2,
                                     int(round(self.canvas_y(i))))
        self.context.stroke()

    def plot_functions(self):
        plots = []
        #logger.debug('plotting functions')
        # precompile the functions
        count = 0
        self.prev_y = []
        for i in self.functions:
            try:
                expression = expressions.convert(i[0])
                #logger.debug(expression)
                compiled = compile(expression, '', 'eval')
                convert_color = lambda color: color / 65535.0
                red = convert_color(i[1].red)
                green = convert_color(i[1].green)
                blue = convert_color(i[1].blue)
                color = (red, green, blue)
                selected = i[-1]
                plots.append((compiled, count, color, selected))
                self.prev_y.append(None)
                count += 1
                #logger.debug('Appended data')
            except Exception, err:
                logger.error(err)
                continue

        if len(plots) != 0:
            #logger.debug('Plots != 0')
            for i in xrange(0, self.canvas_width, self.x_res):
                x = self.graph_x(i + 1)
                for e in plots:
                    #logger.debug(str(e))
                    self.safe_dict['x'] = x
                    try:
                        y = eval(e[0], {'__builtins__': {}}, self.safe_dict)
                        y_c = int(round(self.canvas_y(y)))

                        if y_c < 0 or y_c > self.canvas_height:
                            raise ValueError

                        self.context.set_source_rgb(e[2][0], e[2][1], e[2][2])
                        self.context.set_line_width(2.5 if e[-1] else 1.5)
                        if self.connect_points and\
                           self.prev_y[e[1]] is not None:
                            self.context.move_to(i,
                                                 self.prev_y[e[1]])
                            self.context.line_to(i + self.x_res,
                                                 y_c)
                        else:
                            self.context.move_to(i + self.x_res, y_c)
                            self.context.line_to(i + self.x_res + 1, y_c)
                        self.context.stroke()
                        self.prev_y[e[1]] = y_c
                    except Exception:  # , exc:
                        #logger.debug(exc)
                        #logger.debug('Error at %d: %s' % (x, sys.exc_value))
                        self.prev_y[e[1]] = None
        self.context.set_source_rgb(0, 0, 0)
        self.context.set_line_width(2)
        self.context.rectangle(0,
                               0,
                               self.canvas_width,
                               self.canvas_height)
        self.context.stroke()
        self.context.clip()

    def set_xmax(self, xmax):
        self.xmax = eval(xmax, {'__builtins__': {}}, self.safe_dict)

    def set_xmin(self, xmin):
        self.xmin = eval(xmin, {'__builtins__': {}}, self.safe_dict)

    def set_x_scale(self, xscale):
        self.xscale = eval(xscale, {'__builtins__': {}}, self.safe_dict)

    def set_ymax(self, ymax):
        self.ymax = eval(ymax, {'__builtins__': {}}, self.safe_dict)

    def set_ymin(self, ymax):
        self.ymin = eval(ymax, {'__builtins__': {}}, self.safe_dict)

    def set_y_scale(self, yscale):
        self.yscale = eval(yscale, {'__builtins__': {}}, self.safe_dict)

    def _configure_event_cb(self, widget, event):
        x, y, w, h = widget.get_allocation()
        self.context = widget.get_window().cairo_create()

        # make colors
        self.gc = dict()
        self.layout = pango.Layout(widget.create_pango_context())
        self.canvas_width = w
        self.canvas_height = h
        self.queue_draw()
        return True

    def _expose_event_cb(self, widget, event):
        x, y, w, h = event.area
        window = widget.get_window()
        self.draw_cursor()
        context = window.cairo_create()
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                          w, h)
        self.context = cairo.Context(self.surface)
        context.set_source_surface(self.surface, 0, 0)
        self.draw_queue()
        context.paint()
        return False

    def canvas_y(self, y):
        c_y = (self.ymax - y) * self.canvas_height /\
                    (self.ymax - self.ymin)
        return min(self.canvas_height, max(0, c_y))

    def canvas_x(self, x):
        'Calculate position on canvas to point on graph'
        return (x - self.xmin) * self.canvas_width / (self.xmax - self.xmin)
