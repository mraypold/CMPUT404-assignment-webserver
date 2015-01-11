#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import unittest
import http
import os

class TestHTTP(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        '''Create mock file for using'''
        self.root = os.path.join(os.getcwd())
        self.truefp = os.path.join(self.root, 'testhtml.html')
        self.falsefp = 'mock123.html'

        fp = open(self.truefp, 'w')
        fp.write("<HTML></HTML>")
        fp.close()

    def setUp(self):
        self.protocol = 'HTTP/1.1'
        self.status = '200 OK'
        self.ctype = 'text/html'

        self.m = http.HTTPMessage(
            self.truefp,
            self.protocol,
            self.status,
            self.ctype)

    def test_file_not_exist(self):
        '''Ensure the mock filepath does not actually exist for future tests'''
        self.assertFalse(os.path.isfile(self.falsefp), "File actually exists, tests cannot be run")

    def test_file_exists(self):
        '''Created file in setUpClass exists'''
        self.assertTrue(os.path.isfile(self.truefp), "Mock file does not exists, tests cannot be run")

    def test_IOError_404(self):
        self.assertRaises(IOError, self.m._extract_mbody(self.falsefp), "IOError raise when file does not exist")

        # Header request_status must be updated when a IOError is raised
        status = self.m.header.get_rstatus()
        self.assertTrue(status == 'HTTP/1.1 404 Not Found\r\n')

    @classmethod
    def tearDownClass(self):
        '''Remove test file'''
        os.remove(self.truefp)

if __name__ == '__main__':
    unittest.main()
