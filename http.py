# -*- coding: utf-8 -*-

import time

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
    Length: The length of the message body in bytes that will follow.
    Type: Content type of the message (eg: text/html).
    '''

    header = {
        'request_status':'',
        'date':'Date: ',
        'server':'Server: ',
        'content_length':'Content-Length: ',
        'content_type':'Content-Type: ',
        'blank':'\n'}

    def __init__(self, protocol, status, length, type):
        self.header['request_status'] = protocol + ' ' + status + '\n'

        # May have not been provided length in str format
        self.header['content_length'] += str(length) + '\n'

        self.header['content_type'] += type + '\n'
        self._date()
        self._server()

    def _date(self):
        self.header['date'] += time.strftime('%a, %d %b %Y %H:%M:%S %z') + '\n'

    def _server(self):
        self.header['server'] += 'CMPUT 404 Webserver\n'

    def get_string(self):
        return self.header['request_status'] + self.header['date'] + \
            self.header['server'] + self.header['content_length'] + \
            self.header['content_type'] + self.header['blank']

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
