import os
import pdb
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from artifactory_api import ArtifactoryAPI


class TestArtifactoryAPI(unittest.TestCase):
    def test_init(self):
        aapi = ArtifactoryAPI(configs_file_path=os.path.abspath(os.path.join("files", "config.json")))
        self.assertEqual(aapi.server_name, "test1")

    def test_system_ping(self):
        aapi = ArtifactoryAPI(configs_file_path=os.path.abspath(os.path.join("files", "config.json")))
        aapi.system_ping()
