#!/usr/bin/python3
from websitemixer import app

app.debug = True  # disable if not dev!
app.run(host='0.0.0.0')
