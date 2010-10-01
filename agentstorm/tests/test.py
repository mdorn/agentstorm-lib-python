import os
import unittest

from agentstorm.wrapper import AgentStorm

class TestAgentStormAPI(unittest.TestCase):

    def setUp(self):
        cur_dir = os.path.dirname(__file__.decode('utf-8'))
        f = open('%s/json/properties.json' % cur_dir, 'r')
        self.client = AgentStorm('test', '')
        self.client.file = f

    def test_properties(self):
        resp = self.client.properties.all()
        self.assertEqual(resp.Count, 5)
        
        first_property = resp.Properties[0]
        self.assertEqual(first_property.Id, '106023')        
        self.assertEqual(first_property.StreetName, 'Fox Hill')

if __name__ == "__main__":
    unittest.main()
