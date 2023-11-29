"""
Django command to wait for the database to be available.
"""

import time
from psycopg2 import OperationalError as Psycopg2Error

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database"""

    # handle() is the method that will be executed when we run this command
    def handle(self, *args, **options):
        """Handle the command"""
        # stdout is the standard output to log the output of the command
        self.stdout.write("Waiting for database...")
        db_up = None
        while not db_up:
            try:
                # check() will try to access the database and if \
                # it fails it will raise an OperationalError
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
