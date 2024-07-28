# myapp/management/commands/restartserver.py

from django.core.management.base import BaseCommand
import os
import subprocess
import sys

class Command(BaseCommand):
    help = 'Khởi động lại server phát triển Django'

    def handle(self, *args, **kwargs):
        # Lấy đường dẫn đến file manage.py
        manage_py_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'manage.py')

        # Khởi động lại server
        self.stdout.write('Khởi động lại server...')
        python = sys.executable
        os.execl(python, python, manage_py_path, 'runserver')
