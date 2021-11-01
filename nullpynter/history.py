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

history - class for the history
"""

import json
import os
from pathlib import Path

# Platform-specific data path. This should be relative to the home folder
DATA_PATH = ['.local', 'share']
APP_DIR = 'nullpynter'
HISTFILE = 'history'

class NpyHistory:
    """ A Class to interact with the history of files.
    
    Allows a user to view the history of the files sent through the service. 
    This helps prevent the user needing to upload files multiple times. We can
    also check the history on upload and if a particular file/link was already
    sent, we can fetch the existing URL rather than the old one.
    """

    def __init__(self) -> None:
        data_dir_path = Path.home() / os.path.join(*DATA_PATH) / APP_DIR
        if not data_dir_path.exists():
            data_dir_path.mkdir()
        self._hist_file_path = data_dir_path / HISTFILE
        self._hist_file_path.touch(exist_ok=True)

        self._load_histfile()
    
    def get(self) -> dict:
        """ Get the current history"""
        self._load_histfile()
        return self.history
    
    def append(self, item:str, url:str, response:str) -> None:
        """ Append a responded item to the history
        
        Arguments:
            item - The filename or full-url
            url - The URL of the Nullpointer service
            response - The shortened/uploaded URL
        """
        self._load_histfile()
        try:
            self.history[url][response] = item
        except KeyError:
            self.history[url] = {}
            self.history[url][response] = item
        self._save_histfile()
        
    def pop(self, url:str, item:str='', response:str='') -> tuple:
        """ Find a specified item from the history and return it.

        This removes the item from the history; however, this does *NOT* remove 
        the item from Nullpointer!
        
        Arguments:
            url - The Nullpointer service URL
            item - The item text/path which was sent
            response - The shortened/uploaded URL from Nullpointer
        
        Returns:
            (url:str, response:str, item:str) if the item was found, 
            otherwise ()
        """
        self._load_histfile()
        if response:
            try:
                self._save_histfile()
                return (url, response, self.history[url].pop(response))
            except KeyError:
                self._save_histfile()
                return ()
        
        try:
            for key, value in self.history.items():
                if item == value:
                    self._save_histfile()
                    return (url, key, self.history[url].pop(key))
        except KeyError:
            self._save_histfile()
            return ()
    
    def clear(self, url:str = ''):
        """ Clear all of the history from the file."""
        if url:
            self.history[url].clear()
            self._save_histfile()
            return
        
        self.history.clear()
        self._save_histfile()
        return
    
    def _load_histfile(self):
        """ Load the history file"""
        try:
            with open(self._hist_file_path, mode='r') as hist_file:
                self.history = json.load(hist_file)
        except json.decoder.JSONDecodeError:
            self.history = {}
    
    def _save_histfile(self):
        """ Save the history file"""
        with open(self._hist_file_path, mode='w') as hist_file:
            json.dump(self.history, hist_file, indent=2)
                