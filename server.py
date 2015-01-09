# -*- coding: utf-8 -*-

import SocketServer
import http
import os

# Copyright 2013-2015 Abram Hindle, Eddie Antonio Santos, Michael Raypold
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
#
# StackOverflow Resources
# For overriding SocketServer.TCPServer._init__()
# http://stackoverflow.com/questions/6875599/with-python-socketserver-how-can-i-pass-a-variable-to-the-constructor-of-the-han
# http://stackoverflow.com/questions/3911009/python-socketserver-baserequesthandler-knowing-the-port-and-use-the-port-already
# http://stackoverflow.com/questions/15889241/send-a-variable-to-a-tcphandler-in-python
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class PyServer(SocketServer.TCPServer):
    '''
    Implements a simple server for HTTP/1.1 GET requests.

    Directory tree is built upon server initialization. As such,
    if files are removed or modified during server uptime, unspecified
    behaviour will result.
    '''

    def __init__(self, Host, Port):
        SocketServer.TCPServer.allow_reuse_address = True
        # Create the server, binding to localhost on port 8080
        SocketServer.TCPServer.__init__(self, (HOST, PORT),RequestHandler)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        self.serve_forever()

    def _build_dtree(self):
        '''
        Builds a tree of the directories and files to be served by the
        server.
        '''
        return True

class RequestHandler(SocketServer.BaseRequestHandler):
    '''
    Handles basic HTTP/1.1 requests.

    Overrides SocketServer.TCPServer handle() method.
    '''

    def handle(self):
        self.data = self._extract_request(self.request.recv(1024).strip())
        # self.data = self._extract_request(self.data)

        print ("Got a request of: %s\n" % self.data)
        self.request.sendall(self.data)

    def _extract_request(self, data):
        '''Extract first line from received request'''
        return data.splitlines()[0]

    def _is_path(self, path):
        '''Confirm filepath is legitimate'''
        fp = os.path.join(os.getcwd(), 'www/', path)
        return os.path.isfile(fp)

    # _get_path(), _is_get(), _is_HTTP() assumes standard form
    # eg: GET /index.html HTTP/1.1
    def _get_path(self, request):
        return request.split()[1]

    def _is_get(self, request):
        # return request.strip()[0:3] == 'GET'
        return request.strip().split()[0] == 'GET'

    def _is_HTTP(self, request):
        # return request.strip()[-8:] == 'HTTP/1.1'
        return request.strip().split()[-1] == 'HTTP/1.1'

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    server = PyServer(HOST, PORT)
