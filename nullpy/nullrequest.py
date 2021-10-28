""" Nullpy - The Nullpointer Uploader Service Interface

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

nullrequest.py - base class for any requests to the service
"""

import urllib
import urllib3

class NullRequest:
    """nullrequest - base class for requests to the service
    
    Attributes:
        service_url(int): The url for the null pointer service to use
        request_params (dict): The fields and values for the formdata to send
    """
    http = urllib3.PoolManager()

    def __init__(self, service_url: int = 'http://0x0.st/'):
        """Class constructor
        
        Arguments: 
            service_url(int): The URL for the nullpointer service to use. 
        """
        self.service_url: str = service_url
        self.request_params: dict = {}
    
    def send_request(self):
        """Sends the request out to the service.
        
        Returns:
            The response from the service (usually the URL or an error)
        """
        request = http.request(
            'POST',
            self.service_url,
            fields = self.request_params
        )
        return request.data
    
    @property
    def service_url(self):
        """int: the URL for the service to use."""
        return self._service_url
    
    @service_url.setter
    def service_url(self, url):
        """Sets the service_url. Must be a nullpointer service URL"""
        self._service_url = url