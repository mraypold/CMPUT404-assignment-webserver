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
# For preventing malicous directory traversal
# http://www.guyrutenberg.com/2013/12/06/preventing-directory-traversal-in-python/
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class ServerDirectory():
    '''A directory abstraction to hide operating system calls for the server.

    Arguments:
        root (str): The base directory of the web server
    '''

    def __init__(self, root=os.getcwd()):
        self.root = os.path.abspath(root)

    def get_root(self):
        return self.root

    def get_fsize(self, fp):
        '''Return the filesize in bytes, or -1 if the file doesn't exist'''
        return os.path.getsize(fp) if self.exists(fp) else -1

    def get_file(self, fp):
        '''Returns a string of the specified file'''
        with open(fp, 'r') as fbody:
            efile = fbody.read()
        return efile

    def get_encoded_file(self, fp):
        '''Returns the specified file as an encoded string'''
        return self.get_file(fp).encode('utf-8')

    def exists(self, fp):
        return os.path.isfile(fp)

    def is_directory(self, fp):
        return os.path.isdir(fp)

    def get_ctype(self, fp):
        if fp.endswith('.html'):
            return 'text/html'
        elif fp.endswith('.css'):
            return 'text/css'
        else:
            return 'text/plain'

    def append_index(self, fp):
        return os.path.join(fp, 'index.html')

    def has_index(self, fp):
        '''Returns true if a directory has an index.html that can be served'''
        return self.exists(self.append_index(self, fp))

    def build_abspath(self, path):
        path = os.path.normpath('/' + path).lstrip('/')
        return os.path.join(self.root, path)

    def remove_root(self, path):
        '''Delete the directory root from the specified path.

        Intended to be used before sending out a path in an HTTP 301 redirect
        '''
        length = len(self.root)
        if path[:length] == self.root:
            return path[length:]
        else:
            return path

    def trim_relative_root(self, path):
        try:
            return path[1:] if path[0] == '/' else path
        except IndexError:
            return ''

    def __str__(self): # Not secure
        return self.root

class PyServer(SocketServer.TCPServer):
    '''Implements a simple server for HTTP/1.1 GET requests.

    Arguments:
        Host (str): IP to server from.
        Port (int): endpoint connection for destination address

    '''

    def __init__(self, Host, Port):
        SocketServer.TCPServer.allow_reuse_address = True
        # Create the server, binding to localhost on port 8080
        SocketServer.TCPServer.__init__(self, (HOST, PORT),RequestHandler)

        self.root = os.path.join(os.getcwd(), 'www')
        self.directory = ServerDirectory(self.root)
        self.print_server_stats(Host, Port)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        self.serve_forever()

    def print_server_stats(self, host, port):
        print("-------------------------------------")
        print("CMPUT 410 Webserver")
        print("Address: %s:%s" %(str(host), str(port)))
        print("Current time: %s" % time.strftime('%a, %d %b %Y %H:%M:%S'))
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

        rtype, path, protocol = self._split_request(self.head)

        # Prevent malicous directory traversal
        path = directory.append_index(path) if self._serve_index(path) else path
        path = directory.trim_relative_root(path)
        path = directory.build_abspath(path)

        # print("Got a %(r)s request for %(p)s" %{'r':rtype, 'p':directory.remove_root(path)})

        get = self._is_get(rtype)
        servable = directory.exists(path)

        # Serve a redirect for directory not ending with /
        if directory.is_directory(path) and get:
            self.request.sendall(self._build_redirect(path, directory))
            return

        clength = self.server.directory.get_fsize(path)

        if get and servable:
            m = http.HTTPMessage(protocol, '200', clength, path)
            self.request.sendall(m.get_package())
        elif get and not servable:
            m = http.HTTPMessage(protocol, '404', clength, None)
            self.request.sendall(m.get_package())
        else:
            self.request.sendall('HTTP/1.1 501 Not Implemented\r\n\r\n')

    def _build_redirect(self, fp, directory):
        fp = directory.remove_root(fp)
        fp = directory.append_index(fp)
        return "HTTP/1.1 301 Moved Permanently\r\nLocation: " + fp + '\r\n'

    def _serve_index(self, fp):
        '''Returns True if directory ends with / and an index must be served'''
        return True if fp.strip().endswith('/') else False

    def _extract_head(self, request):
        '''Extract first line from received request'''
        return request.splitlines()[0]

    def _split_request(self, request):
        '''Returns the type (eg GET), file requested and http protocol

        If the request is malformed eg: GET /file.html other.html HTTP/1.1,
        return best guess.
        '''
        # TODO see issues.md issue # 1
        result = request.split()
        return result if len(result) == 3 else (result[0], result[1], result[-1])

    def _is_get(self, request_type):
        return request_type.strip() == 'GET'

    def _is_HTTP(self, protocol):
        return protocol.strip() == 'HTTP/1.1'

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    server = PyServer(HOST, PORT)
