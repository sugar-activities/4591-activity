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

import tempfile
import os
os.environ['PROGRAMRUNNING'] = 'SUGAR'
os.environ['INFO_L10N'] = '1'
import logging
logging.basicConfig(level=logging.DEBUG)
import info
logger = logging.getLogger(info.lower_name)
from gettext import gettext as _

import gtk

from sugar.datastore import datastore
from sugar.activity import activity

try:
    import sweetener
except ImportError:
    import sys
    sys.path.append(os.path.abspath('./sugar'))
    import sweetener

os.environ['DATA_DIR'] = os.path.abspath('./data')

from options import Options
from canvas import Canvas


class Activity(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        self.options = Options(self)
        self.options.show()
        self.set_toolbar_box(self.options)
        self.canvas = Canvas(self.options, self)
        self.canvas.show()
        self.set_canvas(self.canvas)
        self.canvas.new()

    def export(self, widget, data):
        jobject = datastore.create()
        jobject.metadata['title'] = self.metadata['title']
        mime_type = data[1]
        jobject.metadata['mime_type'] = mime_type
        file_path = tempfile.mktemp()
        self.canvas.exports[mime_type](file_path)
        jobject.set_file_path(file_path)
        datastore.write(jobject)

    def read_file(self, path):
        return self.canvas.read_file(path)

    def write_file(self, path):
        return self.canvas.write_file(path)

    def unfullscreen(self):
        # The following line is an adition for Graph Plotter
        self.canvas._resize_queue = self.canvas.previous_size
        activity.Activity.unfullscreen(self)
