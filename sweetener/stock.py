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
logger = logging.getLogger('stock')
import gtk

icon_factory = gtk.IconFactory()

# Set the icon name for the stock items, this is used only in Sugar.
# Associate here every default stock id with an icon name if you need it.
icons = {gtk.STOCK_ADD: 'list-add'}


def register(name, label, accelerator, icon_name):
    if accelerator == None:
        keyval = 0
        mask = 0
    else:
        keyval, mask = gtk.accelerator_parse(accelerator)
    gtk.stock_add([(name, label, mask, keyval, '')])
    if icon_name:
        icon_source = gtk.IconSource()
        icon_source.set_icon_name(icon_name)
        icon = gtk.IconSet()
        icon.add_source(icon_source)
        icon_factory.add(name, icon)
        icon_factory.add_default()
        icons[name] = icon_name


def overwrite_stock(stock_id, new_accelerator):
    info = list(gtk.stock_lookup(stock_id))
    keyval, mask = gtk.accelerator_parse(new_accelerator)
    info[2] = mask
    info[3] = keyval
    logger.debug(str(info))
    gtk.stock_add([(info[0], info[1], info[2], info[3], info[4])])

# Here we overwrite the key accelerators for some stock ids.
# Feel free to add here any other stock id if you need it at your activity,
# and send us a patch.

overwrite_stock(gtk.STOCK_ZOOM_IN, '<Ctrl>plus')
overwrite_stock(gtk.STOCK_ZOOM_OUT, '<Ctrl>minus')
overwrite_stock(gtk.STOCK_ZOOM_100, '<Ctrl>0')
# Key accelerator will be F11 on desktops and <Alt>return on Sugar.
overwrite_stock(gtk.STOCK_FULLSCREEN, '<Alt>Return')
overwrite_stock(gtk.STOCK_ADD, '<Ctrl>A')
overwrite_stock(gtk.STOCK_REMOVE, '<Ctrl>R')
overwrite_stock(gtk.STOCK_SELECT_COLOR, '<Ctrl>L')


def get_label(stock, underline):
    text = gtk.stock_lookup(stock)[1]
    if underline:
        text = text.replace('_', '')
    return text


def get_accelerator(stock):
    return gtk.stock_lookup(stock)[2:-1]
