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

from gettext import gettext as _
import gtk
from sugar.graphics import style
from sugar.graphics.alert import Alert as SugarAlert
from sugar.graphics.alert import NotifyAlert as SugarNotify

from icon import Icon


class Alert(SugarAlert):
    def __init__(self, parent, title, content, mtype):
        SugarAlert.__init__(self)
        self._parent = parent
        if mtype == gtk.MESSAGE_INFO:
            icon = Icon(icon_name='emblem-notification')
            icon.show()
            self.props.icon = icon
            icon.props.pixel_size = style.SMALL_ICON_SIZE * 2
        self.props.title = title
        self.props.msg = content
        ok_icon = Icon(icon_name='dialog-ok')
        self.add_button(gtk.RESPONSE_OK, _('Ok'), ok_icon)
        ok_icon.show()
        self.connect('response', self.remove_myself)

    def remove_myself(self, widget=None, response=None):
        self._parent.remove_alert(self)


class NotifyAlert(SugarNotify):
    def __init__(self, parent, title, content, icon, timeout):
        SugarNotify.__init__(self, timeout)
        self._parent = parent
        self.props.title = title
        self.props.msg = content
        if icon is not None:
            icon = Icon(icon_name=icon)
            icon.show()
            self.props.icon = icon
            icon.props.pixel_size = style.SMALL_ICON_SIZE * 2
        self.connect('response', self.remove_myself)

    def remove_myself(self, widget=None, response=None):
        self._parent.remove_alert(self)
