# contactrow.py
#
# Copyright 2021 SeaDve
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

import datetime

from gi.repository import Gtk

from meowgram.constants import Constants


@Gtk.Template(resource_path=f"{Constants.RESOURCEID}/ui/contactrow.ui")
class ContactRow(Gtk.Box):
    __gtype_name__ = 'ContactRow'

    avatar = Gtk.Template.Child()

    contact_name_label = Gtk.Template.Child()
    last_message_label = Gtk.Template.Child()
    time_label = Gtk.Template.Child()

    read_status = Gtk.Template.Child()
    pin_status = Gtk.Template.Child()
    mute_status = Gtk.Template.Child()
    unread_label = Gtk.Template.Child()

    def __init__(self, dialog_data, **kwargs):
        super().__init__(**kwargs)

        self.contact_name_label.bind_property('label', self.avatar, 'text')
        self.update(dialog_data)

    def update(self, dialog_data):
        self.dialog_data = dialog_data

        self.set_message_status()
        self.set_unread_status()
        self.set_mute_status()

        self.contact_name_label.set_text(self.get_contact_name())
        self.last_message_label.set_text(self.get_last_message())
        self.time_label.set_label(f" • {self.get_last_message_time()}")

    def get_contact_name(self):
        contact_name = getattr(self.dialog_data, 'title',
                               self.dialog_data.name)
        return contact_name

    def get_last_message(self):
        message = self.dialog_data.message
        if message.message is None:
            # TODO add action text
            last_message = "Action"
        else:
            last_message = message.message.split('\n')[0].strip()
        if message.media:
            last_message = "🖼️ Photo"

        if message.out:
            sender_name = "You"
        elif self.dialog_data.is_user:
            sender_name = ""
        else:
            try:
                sender_name = message.sender.first_name
            except AttributeError as error:
                try:
                    sender_name = message.sender.post_author
                except AttributeError as error:
                    sender_name = ""

        return (f"{sender_name}: " if sender_name else "") + last_message

    def get_last_message_time(self):
        last_message_time = self.dialog_data.message.date \
            .replace(tzinfo=datetime.timezone.utc) \
            .astimezone()

        today = datetime.datetime.now().astimezone()
        days_difference = (today - last_message_time).days

        if days_difference < 1:
            # TODO Make this work with military time
            format_string = '%I∶%M %p'  # 08:57 AM
        elif 1 <= days_difference < 7:
            format_string = '%a'  # Fri
        elif days_difference >= 7:
            format_string = '%b %d'  # Apr 08
        return last_message_time.strftime(format_string)

    def get_room_members_count(self):
        try:
            return f"{self.dialog_data.entity.participants_count} members"
        except AttributeError as error:
            return ""

    def set_unread_status(self):
        is_pinned = self.dialog_data.pinned
        unread_count = self.dialog_data.unread_count
        self.unread_label.set_visible(unread_count)
        self.unread_label.set_label(str(unread_count))
        self.pin_status.set_visible(is_pinned)

        if unread_count and is_pinned:
            self.pin_status.set_visible(False)

    def set_message_status(self):
        self.read_status.set_visible(self.dialog_data.message.out)

    def set_mute_status(self):
        self.mute_status.set_visible(
            self.dialog_data.dialog.notify_settings.mute_until)
