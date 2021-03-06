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

        self.length = os.path.getsize(self.truefp)

    def setUp(self):
        self.protocol = 'HTTP/1.1'
        self.status = '200 OK'

        self.m = http.HTTPMessage(
            self.protocol,
            self.status,
            self.length,
            self.truefp)

    # Test that setUpClass executed correctly
    def test_file_not_exist(self):
        '''Ensure the mock filepath does not actually exist for future tests'''
        self.assertFalse(os.path.isfile(self.falsefp), "File actually exists, tests cannot be run")

    def test_file_exists(self):
        '''Created file in setUpClass exists'''
        self.assertTrue(os.path.isfile(self.truefp), "Mock file does not exists, tests cannot be run")
    # End test that setUpClass executed correctly

    def test_no_fp_constructor(self):
        '''A 404 page should be created for the message body when fp not defined'''
        self.m = http.HTTPMessage(self.protocol, self.status, self.length, None)
        ehtml = http.HTMLErrorPage('404').get_page()
        self.assertTrue(ehtml == self.m.get_message_body(), 'The created 404 page does not match that created by HTMLErrorPage()')

    def test_404_update_content_size(self):
        self.m = http.HTTPMessage(self.protocol, self.status, self.length, None)
        bsize = http.HTMLErrorPage('404').get_byte_size()
        self.assertTrue(bsize == self.m.header.get_length(), 'Content lengths for header and message body do not match')

    def test_get_protocol(self):
        header = self.m.get_header()
        self.assertTrue(header.get_protocol() == 'HTTP/1.1', 'Protocol did not split() correctly in get_protocol()')

    def test_IOError_404(self):
        self.assertRaises(IOError, self.m._extract_mbody(self.falsefp), "IOError raise when file does not exist")

        # Header request_status must be updated when a IOError is raised
        status = self.m.header.get_rstatus()
        self.assertTrue(status == 'HTTP/1.1 404 Not Found\r\n', "New status not correctly set after IOError")

    def test_httpstatus_exists(self):
        s = http.HTTPStatus('HTTP/1.1', '200')
        self.assertTrue(s.exists('200'), 'Incorrectly returns that HTTPStatus does not exist')
        self.assertFalse(s.exists('999'), 'Incorrectly returns that HTTPStatus does exist')

    def test_code_not_supported(self):
        '''500 Server Error should be set if the given status code is not supported'''
        s = http.HTTPStatus('HTTP/1.1', '999')
        self.assertTrue(s.get_hstatus() == 'HTTP/1.1 500 Internal Server Error\r\n', 'New status line should have 500 status code')


    @classmethod
    def tearDownClass(self):
        '''Remove test file'''
        os.remove(self.truefp)

if __name__ == '__main__':
    unittest.main()
