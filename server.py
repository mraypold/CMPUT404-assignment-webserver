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
# For searching subdirectories in ServerDirectory() _get_files()
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
    An in memory key/value store of the location of files and their size
    in bytes to prevent unnecessary disk IO when looking for files.

    root: The base directory of the web server
    '''
    directory = {}
    dfsize = -1 # Default file size -1 bytes

    def __init__(self, root=os.getcwd()):
        self.root = root
        self._build_directory()

    def _build_directory(self):
        '''
        Seeks all filepaths (keys) in root and determines their size (values)
        in bytes for entry in the self.directory dictionary.
        '''
        self.directory = dict.fromkeys(self._get_fileset(), self.dfsize)
        self._set_all_fsize()

    def rebuild_directory(self):
        self._build_directory()

    def _get_fileset(self):
        '''Returns a set of all filepaths in subdirectories'''
        fileset = set()

        for directory, folder, files in os.walk(self.root):
            for filename in files:
                rd = os.path.relpath(directory, os.getcwd())
                rf = os.path.join(rd, filename)
                fileset.add(rf)

        return fileset

    def _set_all_fsize(self):
        for key in self.directory:
            self._set_fsize(key)

    def _set_fsize(self, fp):
        self.directory[fp] = os.path.getsize(fp)

    def get_fsize(self, fp):
        return self.directory.get(fp, self.dfsize)

    def get_filepaths(self):
        return self.directory.keys()

    def get_num_files(self):
        return len(self.directory)

    def exists(self, fp):
        return fp in self.directory

    def get_ctype(self, fp):
        if(fp.endswith('.html')):
            return 'text/html'
        elif(fp.endswith('.css')):
            return 'text/css'
        else:
            return 'text/plain'

    def _create_table(self):
        '''Create a table for printing'''
        result = 'Location - (Filesize)\n'
        for k,v in self.directory.items():
            result += str(k) + ' - (' + str(v) + ')\n'
        return result.rstrip()

    def __str__(self):
        return self._create_table()

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
        print("Hosting %d file(s)" % self.directory.get_num_files())
        print(self.directory)
        print("-------------------------------------")


class RequestHandler(SocketServer.BaseRequestHandler):
    '''
    Handles basic HTTP/1.1 requests.

    Overrides SocketServer.TCPServer handle() method.
    '''

    # References the server directory initiated in PyServer.
    def handle(self):
        self.head = self._extract_head(self.request.recv(1024).strip())

        # If can't split into three, the request was malformed. Not 'GET / HTTP/1.1'
        rtype, path, protocol = self._split_request(self.head)

        self.request.sendall(self._build_path(path))

        # print ("Got a request of: %s\n" % self.data)
        # self.request.sendall(self.data)

    def _extract_head(self, request):
        '''Extract first line from received request'''
        return request.splitlines()[0]

    # Potential problem if this is longer than 3 variables....investigate
    def _split_request(self, request):
        '''Returns the type (eg GET), file requested and http protocol'''
        return request.split()

    def _is_get(self, request_type):
        return request_type.strip() == 'GET'

    def _is_HTTP(self, protocol):
        return protocol.strip() == 'HTTP/1.1'

    def _append_index(self, path):
        return os.path.join(path, 'index.html')

    def _trim_relative_root(self, path):
        '''Trim relative root to allow os.join() and directory lookup'''
        try:
            return path[1:] if path[0] == '/' else path
        except IndexError:
            return ''

    def _has_extension(self, path):
        return path.endswith('.html') or path.endswith('.css')

    def _build_path(self, path):
        if(path.endswith('/')): # current path is directory
            path = self._append_index(path)

        path = self._trim_relative_root(path)
        return self._set_relpath(path)

    def _set_relpath(self, path):
        rd = os.path.relpath(self.server.root, os.getcwd())
        rf = os.path.join(rd, path)
        return rf

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    server = PyServer(HOST, PORT)
