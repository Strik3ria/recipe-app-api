from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError

from django.test import TestCase


class CommandTests(TestCase):

    def setUp(self):
        self.connection_handler = (
            'django.db.utils'
            '.ConnectionHandler.__getitem__'
        )
        self.wait_for_db = 'wait_for_db'

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""

        with patch(self.connection_handler) as gi:
            gi.return_value = True
            call_command(self.wait_for_db)
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""

        with patch(self.connection_handler) as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command(self.wait_for_db)
            self.assertEqual(gi.call_count, 6)
