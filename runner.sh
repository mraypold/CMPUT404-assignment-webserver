#!/bin/bash
# Run the webserver, run the tests and kill the webserver!
python server.py &
ID=$!
python freetests.py
python not-free-tests.py
# python test-directory.py
# python test-httpheader.py
# python test-misc.py
kill $ID
#pkill -P $$
