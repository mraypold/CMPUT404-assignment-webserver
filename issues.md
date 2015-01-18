Issues to be handled still
========

Issue 1
--------
Error Handling for def _split_request(self, request) in Server.py

Currently a malformed get request will cause problems.

eg: GET /file.html other.html HTTP/1.1

A best guess is returned, taking the first, second and last values of the line to be the request type, path, and protocol.

However, this will not work if the malformed get is of the type GET HTTP/1.1 (if that is even possible). Thus it does not work for lengths less than three.

Best way to handle is to return a 400 status and have the server send an HTTPHeader with 400 Bad Request.

Current solution has been tested in test-misc.py and works for lengths greater than four.

Should note, that firefox does not allow a request type specified above.
