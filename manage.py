#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(BASE_DIR)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario_django.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        raise ImportError("Django isn't installed. Activate your venv and install requirements.txt")
    execute_from_command_line(sys.argv)
