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

# This file is used only in Sugar.

from gettext import gettext as _

help = [[_('Plotting functions'),
         (_('Append a new function.'), 'gtk-add'),
         (_('Remove a function.'), 'gtk-remove'),
         (_('Choose the color for the selected function.'), 'color-preview')],
        [_('Watching the graph'),
         (_('Zoom into the graph.'), 'zoom-in'),
         (_('Zoom out from the graph.'), 'zoom-out'),
         (_('Reset zoom level.'), 'zoom-original'),
         (_('Customize the scale range. \n\
Remember to press enter after editing the entries.'), 'cell-size'),
  (_('You can zoom in directly into the graph by selecting an area to expand'),
   None),
       (_('Hold the Shift key and move the mouse to traverse the graph.'),
        None),
       (_('Do click for switch between the mouse pointing modes.'), None)],
        [_('Some settings'),
         (_('Connect the plotted points.'), 'connect-points'),
         (_('Show the grid.'), 'insert-table')],
        [_('From algebraic expressions to linear expressions'),
         (_('Division: ') + '/', None),
         (_('Integer division: ') + '//', None),
         (_('Power: ') + '^', None)]
        ]
