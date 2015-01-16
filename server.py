# -*- coding: utf-8 -*-

import SocketServer
import http
import os
import time

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
#
# For overriding SocketServer.TCPServer._init__()
# http://stackoverflow.com/questions/6875599/with-python-socketserver-how-can-i-pass-a-variable-to-the-constructor-of-the-han
# http://stackoverflow.com/questions/3911009/python-socketserver-baserequesthandler-knowing-the-port-and-use-the-port-already
# http://stackoverflow.com/questions/15889241/send-a-variable-to-a-tcphandler-in-python
#
# For searching subdirectories in ServerDirectory() _get_fileset()
# http://stackoverflow.com/questions/1192978/python-get-relative-path-of-all-files-and-subfolders-in-a-directory
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

# To implement still
# - check for file permissions before attempting to access...
# - should SocketServer.TCPServer.allow_reuse_address = True be self.TCPServer.allow_reuse_address = True ?
# - update ServerDirectory whenever files are added. Or through infinite loop.
# - Change serverdirectory to seperate thread so that it can be modified when files update or overwrite serverforever()
# - If can't split into three, the request was malformed. Not 'GET / HTTP/1.1' - do error checking

class ServerDirectory():
    '''
    A directory abstraction to hide operating system calls for the server.
    root: The base directory of the web server
    '''

    def __init__(self, root=os.getcwd()):
        self.root = root

    def get_fsize(self, fp):
        return os.path.getsize(fp)

    def get_file(self, fp):
        '''Returns a string of the specified file'''
        with open(fp, 'r') as fbody:
            efile = fbody.read()
        return efile

    def get_encoded_file(self, fp):
        return self.get_file(fp).encode('utf-8')

    def exists(self, fp):
        return os.path.isfile(fp)

    def is_directory(self, fp):
        return os.path.isdir(fp)

    def get_ctype(self, fp):
        if(fp.endswith('.html')):
            return 'text/html'
        elif(fp.endswith('.css')):
            return 'text/css'
        else:
            return 'text/plain'

    def append_index(self, fp):
        return os.path.join(fp, 'index.html')

    def has_index(self, fp):
        '''Returns true if a directory has an index.html that can be served'''
        nfp = self.append_index(self, fp)
        return self.exists(nfp)

    def get_abspath(self, path):
        return os.path.join(self.root, path)

    def trim_relative_root(self, path):
        try:
            return path[1:] if path[0] == '/' else path
        except IndexError:
            return ''

    def __str__(self, fp):
        return self.root

class PyServer(SocketServer.TCPServer):
    '''
    Implements a simple server for HTTP/1.1 GET requests.
    '''

    def __init__(self, Host, Port):
        SocketServer.TCPServer.allow_reuse_address = True
        # Create the server, binding to localhost on port 8080
        SocketServer.TCPServer.__init__(self, (HOST, PORT),RequestHandler)

        self.root = os.path.join(os.getcwd(), 'www')
        self.directory = ServerDirectory(self.root)
        self.print_server_stats()

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        self.serve_forever()

    def print_server_stats(self):
        print("-------------------------------------")
        print("CMPUT 410 Webserver")
        print("Current time: %s" % time.strftime('%a, %d %b %Y %H:%M:%S'))
        print("Root directory: %s" % self.root)
        print("-------------------------------------")

class RequestHandler(SocketServer.BaseRequestHandler):
    '''
    Handles basic HTTP/1.1 requests.

    Overrides SocketServer.TCPServer handle() method.
    '''

    # References the server directory initiated in PyServer.
    def handle(self):
        self.head = self._extract_head(self.request.recv(1024).strip())

        directory = self.server.directory

        # If can't split into three, the request was malformed. Not 'GET / HTTP/1.1' - TODO Handle this error
        rtype, path, protocol = self._split_request(self.head)

        # path = self._build_path(path)
        print("Given: " + path)
        path = directory.trim_relative_root(path)
        print("Trim: " + path)
        path = directory.get_abspath(path)
        print("Final: " + path)

        if(directory.is_directory(path)):
            path = directory.append_index(path)
            print("Append: " + path)

        servable = directory.exists(path)
        get = self._is_get(rtype)

        print("Got a %(r)s request for %(p)s" %{'r':rtype, 'p':path})

        clength = self.server.directory.get_fsize(path)

        if(get and servable):
            m = http.HTTPMessage(protocol, '200 OK', clength, path)
            self.request.sendall(m.get_package())
        elif(get and not servable):
            m = http.HTTPMessage(protocol, '404 Not Found', clength, None)
            self.request.sendall(m.get_package())
        else:
            m = http.HTTPMessage(protocol, '404 Not Found', clength, None) # In actuality this is not a 404 error. Server only supports GET TODO
            self.request.sendall(m.get_package())

    def _extract_head(self, request):
        '''Extract first line from received request'''
        return request.splitlines()[0]

    def _split_request(self, request):
        '''Returns the type (eg GET), file requested and http protocol'''
        return request.split()

    def _is_get(self, request_type):
        return request_type.strip() == 'GET'

    def _is_HTTP(self, protocol):
        return protocol.strip() == 'HTTP/1.1'

    # def _append_index(self, path):
    #     return os.path.join(path, 'index.html')

    # def _has_extension(self, path):
    #     return path.endswith('.html') or path.endswith('.css')

    # def _build_path(self, path):
    #     if(path.endswith('/')): # current path is directory
    #         path = self._append_index(path)
    #
    #     path = self._trim_relative_root(path)
    #     return self._set_relpath(path)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    server = PyServer(HOST, PORT)
