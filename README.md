CMPUT404-assignment-webserver
=============================

CMPUT404-assignment-webserver

See requirements.org (plain-text) for a description of the project.

Make a simple webserver.

Contributors / Licensing
========================

Forked from [CMPUT404-assignment-webserver]

[CMPUT404-assignment-webserver]:https://github.com/abramhindle/CMPUT404-assignment-webserver

Additional contributions from:

* Michael Raypold

Previous licensing and contribtions as follows:

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle.

server.py, freetests.py and not-free-tests.py contains contributions from:

* Abram Hindle
* Eddie Antonio Santos

But the server.py example is derived from the python documentation
examples thus some of the code is Copyright © 2001-2013 Python
Software Foundation; All Rights Reserved under the PSF license (GPL
compatible) http://docs.python.org/2/library/socketserver.html

External Sources
========================
StackOverflow Resources
For overriding SocketServer.TCPServer._init__()
* [Pass variables](http://stackoverflow.com/questions/6875599/with-python-socketserver-how-can-i-pass-a-variable-to-the-constructor-of-the-han)
* [Request handler](http://stackoverflow.com/questions/3911009/python-socketserver-baserequesthandler-knowing-the-port-and-use-the-port-already)
* [Pass variable to TCP handler](http://stackoverflow.com/questions/15889241/send-a-variable-to-a-tcphandler-in-python)

For searching subdirectories in ServerDirectory() _get_fileset().
*This code eventually got refactored out, but is in earlier commits.*
* [Relative paths of directories](http://stackoverflow.com/questions/1192978/python-get-relative-path-of-all-files-and-subfolders-in-a-directory)

For preventing malicous directory traversal
* [Directory traversal](http://www.guyrutenberg.com/2013/12/06/preventing-directory-traversal-in-python/)
