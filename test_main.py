import json,unittest
from pathlib import Path
from main import *
class Tests(unittest.TestCase):
 def sample(self):return json.loads(Path(__file__).with_name("sample-input.json").read_text())

 def test_distance(self):
  self.assertEqual([x["distance"] for x in run(self.sample())["impacts"][0]["affected"]],[0,1,2,3,3])
 def test_critical(self):self.assertEqual(run(self.sample())["critical_nodes"][0]["downstream_count"],4)
 def test_cycle(self):
  d=self.sample();d["edges"].append({"from":"xr-view","to":"twin-api"});self.assertTrue(run(d)["cycles"])
 def test_bad(self):
  d=self.sample();d["nodes"].append(d["nodes"][0])
  with self.assertRaises(ValueError):run(d)

if __name__=="__main__":unittest.main()
