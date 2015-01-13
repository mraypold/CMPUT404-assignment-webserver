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

    def __init__(self, protocol, status, ctype, length):
        self.header = OrderedDict((
            ('request_status',''),
            ('date','Date: '),
            ('server','Server: CMPUT 404 Webserver\r\n'),
            ('content_type','Content-Type: '),
            ('content_length','Content-Length: '),
            ('blank','\r\n')))

        self.set_status(protocol, status)
        self.set_content_type(ctype)
        self.set_date()
        self.set_length(length)

    def set_status(self, protocol, status):
        self.header['request_status'] = protocol + ' ' + status + '\r\n'

    def set_content_type(self, ctype):
        self.header['content_type'] = 'Content-Type: %s\r\n' %ctype

    def set_date(self):
        self.header['date'] = 'Date: %s\r\n' %time.strftime('%a, %d %b %Y %H:%M:%S %z')

    def set_length(self, length):
        self.header['content_length'] = 'Content-Length: %s\r\n' %str(length)

    def get_length(self):
        return int(self.header.get('content_length').split()[1])

    def get_protocol(self):
        return self.get_rstatus().split()[0]

    def get_rstatus(self):
        return self.header.get('request_status')

    def get_ctype(self):
        return self.header.get('content_type').split()[1]

    def _get_keys(self):
        return self.header.keys()

    def _get_values(self):
        return self.header.values()

    def get_string(self):
        return ''.join(self._get_values())

    def __str__(self):
        return self.get_string()

class HTTPMessage():
    '''
    Packages an HTTP header and the optional HTTP message body data.

    Protocol: The HTTP protocol (eg: HTTP/1.1).
    Status: A valid HTTP status code (No checking is performed. eg: 200 OK).
    fp: The filepath of the file to be included in the HTTP response.

    The given filepath is assumed to be valid and should be checked prior to
    calling HTTPMessage().
    '''

    def __init__(self, protocol, status, length, fp=None):
        self.mbody = ''

        if(fp is None):
            self.header = HTTPHeader(protocol, status, 'text/html', length)
            self._create_404()
        else:
            self.header = HTTPHeader(protocol, status, self.get_ctype(fp), length)
            self._extract_mbody(fp)

    def get_ctype(self, fp):
        if(fp.endswith('.html')):
            return 'text/html'
        elif(fp.endswith('.css')):
            return 'text/css'
        else:
            return 'text/plain'

    def _extract_mbody(self, fp):
        '''Extract file contents into the HTTPMessage'''
        try:
            with open(fp, 'r') as fbody:
                self.mbody = fbody.read()
        except IOError: # File not accessile.
            self._create_404()

    def _create_404(self):
        page = HTMLErrorPage('404')
        self.mbody = page.get_page()
        self.header.set_status(self.header.get_protocol(), '404 Not Found')
        self.header.set_length(str(page.get_byte_size()))

    def get_header(self):
        return self.header

    def get_message_body(self):
        return self.mbody.encode('utf-8')

    def get_package(self):
        '''Combines the header and message for an outgoing HTTP response'''
        result = self.header.get_string() + self.mbody
        return result.encode('utf-8')

    def __str__(self):
        return self.get_package()

class HTMLPage():
    '''Extremely simple HTML page builder'''

    def __init__(self, title):
        self.contents = {
            'doctype':'<!DOCTYPE html>',
            'title':'',
            'body':''}
        self.set_title(title)

    def set_title(self, newtitle):
        self.contents['title'] = newtitle

    def get_title(self):
        return self.contents.get('title')

    def get_doctype(self):
        return self.contents.get('doctype')

    def get_body(self):
        return self.contents.get('body')

    def _get_htag(self, size):
        '''Returns a tuple of opening/closing header tags'''
        return '<h' + str(size) + '>', '</h' + str(size) + '>'

    def _get_ptag(self):
        '''Returns a tuple of opening/closing paragraph tags'''
        return '<p>', '</p>'

    def add_heading(self, heading, size):
        tags = self._get_htag(size)
        self.contents['body'] = self.contents.get('body') + tags[0] + str(heading) + tags[1] + '\n'

        # self.contents['body'] += tags[0] + str(heading) + tags[1] + '\n'

    def add_paragraph(self, text):
        tags = self._get_ptag()
        self.contents['body'] += tags[0] + str(text) + tags[1] + '\n'

    def get_page(self):
        page = self.get_doctype() + '\n'
        page += '<html>\n'
        page += '<head><title>' + self.get_title() + '</title></head>\n'
        page += '<body>\n'
        page += self.get_body()
        page += '</body>\n'
        page += '</html>'
        return page

    def __str__(self):
        return self.get_page()

class HTMLErrorPage(HTMLPage):
    '''
    Creates an error page

    Error codes taken from http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html

    Any errors in generation will automatically cause a 500:Internal Server
    Error page to be generated.

    Takes as input an error code in str or int format
    '''

    # All error codes the server will support/return
    errors = {
        '400':'Bad Request',
        '401':'Unauthorized',
        '402':'Forbidden',
        '404':'Not Found',
        '500':'Internal Server Error',
        '505':'HTTP Version Not Supported'}

    code = '500'

    def __init__(self, code):
        if not (self.is_error(str(code))):
            self.code = '500'
        else:
            self.code = code

        HTMLPage.__init__(self, self.get_error(str(code)))
        self.add_heading()
        self.add_paragraph()

    def add_heading(self, size=4):
        HTMLPage.add_heading(self, self.code, size)

    def add_paragraph(self, text=None):
        if(text is None):
            text = self.get_error(self.code)
        HTMLPage.add_paragraph(self, text)

    def is_error(self, code):
        return code in self.errors

    def get_error(self, code):
        return self.errors.get(str(code), self.errors.get('500'))

    def get_byte_size(self):
        return len(self.get_page().encode('utf-8'))

    def get_page(self):
        return HTMLPage.get_page(self).encode('utf-8')

    def __str__(self):
        return HTMLPage.__str__(self)
