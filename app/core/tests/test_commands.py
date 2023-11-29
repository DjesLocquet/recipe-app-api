"""
Test custom Django management commands
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for db when db is available."""
        patched_check.return_value = True

        call_command("wait_for_db")

        # Check that the command has been called once
        patched_check.assert_called_once_with(databases=["default"])

    # We don't want to sleep during tests, so we mock the sleep function
    @patch("time.sleep", return_value=None)
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db when getting OperationalError."""
        # The first 2 times we call check() we raise an Psycopg2Error \
        # the next 3 times we raise a OperationalError
        # Then we return True to simulate the database is ready
        patched_check.side_effect = [Psycopg2Error] * 2 + \
                                    [OperationalError] * 3 + [True]

        call_command("wait_for_db")

        self.assertEqual(patched_check.call_count, 6)

        # command will be called multiple times until it is successful
        patched_check.assert_called_with(databases=["default"])
