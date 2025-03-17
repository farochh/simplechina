#!/usr/bin/env python3
import sys
import os
from flup.server.fcgi import WSGIServer

sys.path.insert(0, '/.local/lib/python3.10/site-packages')  # Путь к установленным библиотекам

from app import app  # Импорт вашего Flask-приложения

sys.stdout = sys.stderr
os.chdir(os.path.dirname(__file__))

WSGIServer(app).run()
