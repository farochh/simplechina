import sys
import os

# Указываем путь к проекту
sys.path.insert(0, '/home/c/cm41785/adminka/public_html')

# Указываем путь к библиотекам виртуального окружения
sys.path.insert(1, '/home/c/cm41785/adminka/public_html/venv/lib/python3.10/site-packages')

# Импортируем приложение Flask
from app import app as application
