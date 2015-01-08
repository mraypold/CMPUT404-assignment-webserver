#!/bin/bash
# Run the webserver, run the tests and kill the webserver!
python server.py &
ID=$!
python tests/freetests.py
python tests/not-free-tests.py
kill $ID
#pkill -P $$
