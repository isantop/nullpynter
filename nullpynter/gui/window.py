""" Nullpynter - The Nullpointer Uploader Service Interface

BSD 3-Clause License

Copyright (c) 2021, Ian Santopietro
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import gi
gi.require_versions(
    {
        'Gdk': '4.0',
        'Gtk': '4.0',
        'GLib': '2.0',
        'Pango': '1.0',
    }
)

from gi.repository import Gdk, Gtk

from .enums import Action
from .headerbar import Headerbar
from .threads import ServiceThread

IMAGE_FILETYPES = [
    'jpg',
    'jpeg',
    'jpe',
    'jif',
    'jfif',
    'jfi',
    'png',
    'gif',
    'webp',
    'tiff',
    'tif',
    'bmp',
    'dib',
]

class NpyWindow(Gtk.ApplicationWindow):
    """Main Window"""

    def __init__(self, application=None, pool=None) -> None:
        super().__init__(application=application)
        self.http = pool
        self.set_title('Nullpynter')
        self.action = None

        self.headerbar = Headerbar()
        self.set_titlebar(self.headerbar)

        self.content_grid = Gtk.Grid()
        self.content_grid.props.margin_start = 12
        self.content_grid.props.margin_end = 12
        self.content_grid.props.margin_top = 12
        self.content_grid.props.margin_bottom = 12
        self.content_grid.props.row_spacing = 6
        self.content_grid.props.column_spacing = 6
        self.content_grid.set_hexpand(True)
        self.set_child(self.content_grid)

        entry_label = Gtk.Label.new('Item to upload')
        self.content_grid.attach(entry_label, 0, 1, 1, 1)

        entry_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        Gtk.StyleContext.add_class(entry_box.get_style_context(), 'linked')
        self.content_grid.attach(entry_box, 1, 1, 1, 1)

        self.item_entry = Gtk.Entry()
        self.item_entry.set_hexpand(True)
        self.item_entry.connect('changed', self.set_action_button_text)
        entry_box.append(self.item_entry)

        self.chooser_button = Gtk.Button.new_with_label('Browse')
        entry_box.append(self.chooser_button)

        url_label = Gtk.Label.new('Service URL')
        self.content_grid.attach(url_label, 0, 4, 1, 1)

        response_image = Gtk.Image.new_from_icon_name('go-down-symbolic')
        self.content_grid.attach(response_image, 1, 2, 1, 1)

        self.busy_spinner = Gtk.Spinner()
        self.content_grid.attach(self.busy_spinner, 0, 3, 1, 1)

        self.response_entry = Gtk.Entry()
        self.response_entry.set_hexpand(True)
        self.response_entry.set_editable(False)
        # FIXME: Figure out how to clipboard
        # self.response_entry.set_icon_from_icon_name(
        #     Gtk.EntryIconPosition.SECONDARY,
        #     'edit-copy-symbolic'
        # )
        # self.response_entry.set_icon_activatable(
        #     Gtk.EntryIconPosition.SECONDARY,
        #     True
        # )
        # self.response_entry.connect(
        #     'icon-release', 
        #     self.put_response_in_clipboard,
        #     self
        # )
        self.content_grid.attach(self.response_entry, 1, 3, 1, 1,)

        self.url_entry = Gtk.Entry()
        self.url_entry.set_hexpand(True)
        self.url_entry.set_text('http://0x0.st')
        self.url_entry.set_placeholder_text('Nullpointer service URL')
        self.url_entry.set_width_chars(20)
        self.content_grid.attach(self.url_entry, 1, 4, 1, 1)

        self.headerbar.action_button.connect('clicked', self.action_button_clicked)

    def set_action_button_text(self, widget, data=None):
        """ Sets the text in the action button.
        
        We set theis based on the contents of the entry, since we do different 
        actions based on what the user is sending.
        """
        print(f'Current Action: {self.action}')

        item_text = self.item_entry.get_text()
        if not item_text.startswith('http'):
            print('Item is local file')
            self.action = Action.UPLOAD
            print(f'Action now is {self.action}')
        else:
            print('Item is URL')
            item_ext = item_text.split('.')[-1]
            print(f'item extension: {item_ext}')
            if item_ext.lower() in IMAGE_FILETYPES:
                print('Item is remote image')
                self.action = Action.REMOTE
                print(f'Action now is {self.action}')
            else:
                print('Item is long URL')
                self.action = Action.SHORTEN
                print(f'Action now is {self.action}')

        self.headerbar.action_button.set_label(self.action.label())

    def put_response_in_clipboard(self, widget=None, data=None, extra=None):
        """ Puts the contents of the response entry into the clipboard"""
        clipboard = self.response_entry.get_clipboard()
        clipboard.set_text(self.response_entry.get_text())     

    def action_button_clicked(self, widget, data=None):
        self.set_sensitive(False)
        self.busy_spinner.start()
        service = ServiceThread(self)
        service.start()
