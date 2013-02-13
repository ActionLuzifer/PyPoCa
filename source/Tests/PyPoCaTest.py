import os
import unittest
import source.PyPoCa as PyPoCa


class PyPoCaTestCase(unittest.TestCase):
    configxmlname = os.path.normpath("{0}/config_memorydb.xml".format(os.getcwd()))
    def setUp(self):
        self.pypoca = PyPoCa.PyPoCa(self.configxmlname)
    
    
    def tearDown(self):
        self.pypoca = None
        
    
    def test_configname(self):
        self.assertEqual(self.pypoca.STR_configxmlFilename, self.configxmlname, "Pfad/Name der Configdatei stimmt nicht überein")