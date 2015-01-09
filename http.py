# -*- coding: utf-8 -*-

import time
from collections import OrderedDict

# Copyright 2015 Michael Raypold
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html

class HTTPHeader():
    '''
    Builds an HTTP header response.

    Protocol: The HTTP protocol (eg: HTTP/1.1).
    Status: A valid HTTP status code (No checking is performed. eg: 200 OK).
    Type: Content type of the message (eg: text/html).

    See http://en.wikipedia.org/wiki/HTTP_message_body
    '''

    header = OrderedDict((
        ('request_status',''),
        ('date','Date: '),
        ('server','Server: CMPUT 404 Webserver\n'),
        ('content_type','Content-Type: '),
        ('blank','\n')))

    def __init__(self, protocol, status, ctype):
        self.set_status(protocol, status)
        self.set_content_type(ctype)
        self.set_date()

    def set_status(self, protocol, status):
        self.header['request_status'] = protocol + ' ' + status + '\n'

    def set_content_type(self, ctype):
        self.header['content_type'] += ctype + '\n'

    def set_date(self):
        self.header['date'] += time.strftime('%a, %d %b %Y %H:%M:%S %z') + '\n'

    def get_string(self):
        return ''.join(self._get_values())

    def _get_keys(self):
        return self.header.keys()

    def _get_values(self):
        return self.header.values()

    def __str__(self):
        return self.get_string()

class HTTPMessage():
    '''
    Packages an HTTP header and the optional HTTP message body data.

    fp: The filepath of the file to be included in the HTTP response.
    '''

    fp = ''

    def __init__(self, fp):
        self.fp = fp

    def build_header(self, protocol, status):
        return

    def build_message(self):
        return

    def build_package(self):
        '''Combines the header and message for an outgoing HTTP response'''
        return

    def get_size(self, path):
        '''Takes the filepath and return the size (in bytes) of the file'''
        return
