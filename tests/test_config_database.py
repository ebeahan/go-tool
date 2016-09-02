import unittest
import sys

sys.path.insert(0, '..')
from go.go import ConfigDatabase

class TestConfigDatabase(unittest.TestCase):

    MENU_DISPLAY = """
 Make a selection or use Ctrl+C to exit.
############################################

1) host1.example.com
2) host2.example.com
"""

    def setUp(self):
        self.configdb = ConfigDatabase('test-config.db')
        self.configdb.update_new_entry("host1.example.com",
                               22,
                               "admin",
                               "10.0.0.1",
                               description="This is a test host.")
        self.configdb.update_new_entry("host2.example.com",
                                       2222,
                                       "root",
                                       "192.168.1.50",
                                       description="This is another host.")

        self.menu_display = """
 Make a selection or use Ctrl+C to exit.
############################################

1) host1.example.com
2) host2.example.com
"""

    def tearDown(self):
        pass

    def test_lookup_entry_method(self):
        result = self.configdb.lookup_entry("host1.example.com")
        self.assertEquals(result.hostname, "host1.example.com")
        self.assertEquals(result.ip, "10.0.0.1")
        self.assertEquals(result.username, "admin")
        self.assertEquals(result.port, 22)

    def test_lookup_id_method(self):
        result = self.configdb.lookup_id(2)
        self.assertEquals(result.id, 2)

    def test_menu_display(self):
        self.configdb.remove_entry(1)
        with self.assertRaises(AttributeError):
           self.configdb.lookup_id(1).id
    