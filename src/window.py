# window.py
#
# Copyright 2021 mew
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
gi.require_version('Gdk', '3.0')
gi.require_version('Handy', '1')
from gi.repository import Gdk, Gio, GLib, Gtk, Handy


@Gtk.Template(resource_path='/com/github/ExposedCat/Meowgram/ui/window.ui')
class MeowgramWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'MeowgramWindow'

    headerbar_group = Gtk.Template.Child()
    main_leaflet = Gtk.Template.Child()
    contacts_listbox = Gtk.Template.Child()
    message_box = Gtk.Template.Child()

    back_button = Gtk.Template.Child()

    menu_button = Gtk.Template.Child()
    submenu_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.main_leaflet.bind_property("folded", self.back_button, "visible")
        self.main_leaflet.bind_property("folded", self.headerbar_group, "decorate-all")

        for index in range(10):
            self.contacts_listbox.insert(ContactRow(), -1)
            if index % 2:
                self.message_box.add(MessageRow(1))
            else:
                self.message_box.add(MessageRow(0))

    @Gtk.Template.Callback()
    def on_back_button_clicked(self, widget):
        self.main_leaflet.set_visible_child_name("contacts_pane")


@Gtk.Template(resource_path='/com/github/ExposedCat/Meowgram/ui/contact.ui')
class ContactRow(Handy.ActionRow):
    __gtype_name__ = 'ContactRow'

    time_label = Gtk.Template.Child()
    avatar = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_prefix(self.avatar)
        self.set_title("USERNAME")
        self.set_subtitle("Hello There")
        self.time_label.set_label("22∶05")


@Gtk.Template(resource_path='/com/github/ExposedCat/Meowgram/ui/message.ui')
class MessageRow(Gtk.Box):
    __gtype_name__ = 'MessageRow'

    avatar = Gtk.Template.Child()
    message_label = Gtk.Template.Child()

    def __init__(self, is_from_self, **kwargs):
        super().__init__(**kwargs)

        self.message_style_context = self.message_label.get_style_context()

        if is_from_self:
            self.set_from_self_mode()
        else:
            self.set_from_contact_mode()

    def set_from_self_mode(self):
        self.avatar.set_visible(False)
        self.message_label.set_margin_start(72)
        self.message_label.set_halign(Gtk.Align.END)
        self.message_label.set_justify(Gtk.Justification.RIGHT)
        self.message_style_context.add_class("message-out")
        self.message_style_context.remove_class("message-in")


    def set_from_contact_mode(self):
        self.avatar.set_visible(True)
        self.message_label.set_margin_end(72)
        self.message_label.set_halign(Gtk.Align.START)
        self.message_label.set_justify(Gtk.Justification.LEFT)
        self.message_style_context.add_class("message-in")
        self.message_style_context.remove_class("message-out")
        
