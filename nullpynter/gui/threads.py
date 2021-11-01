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
import time
from threading import Thread
from gi.repository import GLib

from .enums import Action
from ..remote import Remote
from ..shorten import Shorten
from ..upload import Upload

class InfoThread(Thread):

    def __init__(self, url, widget, pool):
        super().__init__()
        self.url = url
        self.wigdet = widget
        self.http = pool

    def run(self):
        icon_request = self.http.request(
            'GET',
            self.url
        )
        icon_text = icon_request.data.decode('UTF-8').strip()
        GLib.idle_add(self.wigdet.set_markup, icon_text)

class ServiceThread(Thread):
    
    def __init__(self, widget):
        super().__init__()
        self.wigdet = widget
        self.http = widget.http
    
    def run(self):
        action_map = {
            Action.UPLOAD: self.upload,
            Action.REMOTE: self.remote,
            Action.SHORTEN: self.shorten
        }
        item_text = self.wigdet.item_entry.get_text()
        service_url = self.wigdet.url_entry.get_text()
        service_action = self.wigdet.action.value
        print(f'Sending {item_text} to {service_url} for {self.wigdet.action}')
        
        response = action_map[self.wigdet.action](item_text, service_url)

        GLib.idle_add(self.wigdet.response_entry.set_text, response)
        GLib.idle_add(self.wigdet.set_sensitive, True)
        GLib.idle_add(self.wigdet.busy_spinner.stop)
    
    def shorten(self, item, url):
        short = Shorten(service_url=url)
        short.set_request_params(item)
        return short.send_request()
        
    def remote(self, item, url):
        rem = Remote(service_url=url)
        rem.set_request_params(item)
        return rem.send_request()
        
    def upload(self, item, url):
        return 'Not Implemented!'