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
import urllib3

from threading import Thread
from gi.repository import GLib, Gtk, Pango


http = urllib3.PoolManager()

class Headerbar(Gtk.HeaderBar):
    """Application headerbar"""

    def __init__(self, url:str = "http://0x0.st") -> None:
        GLib.threads_init()
        super().__init__()
        self.url = url
        self.info:str = 'Fetching info from service...'

        info_button = Gtk.ToggleButton.new()
        info_button.set_icon_name('dialog-information-symbolic')
        info_button.connect('toggled', self.show_hide_popover)

        # self.pack_end(info_button)

        self.info_popover = Gtk.Popover.new()

        info_scroller = Gtk.ScrolledWindow()
        self.info_popover.set_child(info_scroller)

        self.info_label = Gtk.Label.new(self.info)
        self.info_label.set_wrap(True)
        self.info_label.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
        info_scroller.set_child(self.info_label)
        # self.info_popover.show()
        # self.update_info()

    def update_info(self):
        """Update the text in the info_label"""
        info_thread = InfoThread(self.url, self.info_label)
    
    def show_hide_popover(self, widget, data=None):
        print('showing/hiding popover')
        if widget.get_active():
            self.info_popover.popup()
        else:
            self.info_popover.popdown()

class InfoThread(Thread):

    def __init__(self, url, widget):
        super().__init__()
        self.url = url
        self.wigdet = widget

    def run(self):
        icon_request = http.request(
            'GET',
            self.url
        )
        icon_text = icon_request.data.decode('UTF-8').strip()
        GLib.idle_add(self.wigdet.set_markup, icon_text)
