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
import server
import os

class TestDirectory(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        '''Create test directory and file'''
        self.root = os.path.join(os.getcwd())
        self.testroot = os.path.join(self.root, 'testdir')
        self.testsubdir = os.path.join(self.testroot, 'subdir')

        os.mkdir(self.testroot)
        os.mkdir(self.testsubdir)

        self.filename = os.path.join(self.testroot, 'hello.html')
        self.subfilename = os.path.join(self.testsubdir, 'hello2.html')

        for path in (self.filename, self.subfilename):
            fp = open(path, 'w')
            fp.write("<HTML></HTML>")
            fp.close()

        self.d = server.ServerDirectory(self.testroot)


    def test_directory_created(self):
        '''setUpClass should create subdirectory'''
        self.assertTrue(os.path.exists(self.testroot), "Subdirectory does not exist!")

    def test_file_created(self):
        '''setUpClass should create a temporary file for use'''
        self.assertTrue(os.path.isfile(self.filename), "File does not exist!")

    def test_file_in_directory(self):
        '''Directory must state that a file exists'''
        self.assertTrue(self.d.exists('testdir/hello.html'), "Directory should return that the file exists")

    def test_file_not_directory(self):
        '''Directory must state that a file does not exist'''
        self.assertFalse(self.d.exists('testdir/notexist.html'), "Directory should return that file does not exist")

    def test_number_files(self):
        '''There should be exactly 2 files detected by ServerDirectory'''
        self.assertTrue(self.d.get_num_files() == 2, "ServerDirectory miscounted the number of files")

    def test_get_filepaths(self):
        '''The filepaths should be of the form self.testroot/.'''
        paths = self.d.get_filepaths()
        for path in paths:
            self.assertTrue(path[0:7] == self.testroot[-7:], "The filepaths do not start with the correct root directory")

    def test_get_fsize(self):
        '''ServerDirectory should return correct fsize(bytes) for specified path'''
        self.assertTrue(self.d.get_fsize('testdir/hello.html') == 13, "Did not get the correct file size")

    def test_content_type(self):
        '''If an html file type, text/html should be the returned content type'''
        self.assertTrue(self.d.get_ctype('testdir/hello.html') == 'text/html', "Content type does not match file extension")

    @classmethod
    def tearDownClass(self):
        '''Remove test directory and file'''
        os.remove(self.filename)
        os.remove(self.subfilename)
        os.rmdir(self.testsubdir)
        os.rmdir(self.testroot)


if __name__ == '__main__':
    unittest.main()
