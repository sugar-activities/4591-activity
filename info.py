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

service_name = 'org.sugarlabs.GraphPlotter'

import os
this_dir = os.path.abspath('./')

import gettext
if int(os.environ['INFO_L10N']):
    locale_path = os.path.join(this_dir, 'locale')
    gettext.bindtextdomain(service_name, locale_path)
    gettext.textdomain(service_name)
_ = gettext.gettext


DOCUMENT = 0
CONFIG = 1
io_mode = DOCUMENT

name = _('Graph Plotter')
generic_name = _('Mathematical Function Plotter')
lower_name = 'graph-plotter'
copyright = 'Copyright © 2012 Daniel Francis'
version = '9'
description = _("Plot mathematical functions and study maths.")
authors = ['Daniel Francis <francis@sugarlabs.org>']
#TRANS: The link to the translated page if any, if not leave the string as it is
url = _('http://wiki.sugarlabs.org/go/Activities/Graph_Plotter')
documentation = _('http://wiki.sugarlabs.org/go/Activities/Graph_Plotter')
categories = ['Education', 'Math']

file_filter_name = _('Plotted Functions')
file_filter_mime = 'application/x-%s' % lower_name
file_filter_patterns = ['*.gpt']

# Refer to the COPYING
license = 'GPLv3'
license_file = open('COPYING')
license_content = license_file.read()
license_file.close()
