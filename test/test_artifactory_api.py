import os
import pdb
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from artifactory_api import ArtifactoryAPI, EXPOSED_API


class TestArtifactoryAPI(unittest.TestCase):
    def test_init(self):
        aapi = ArtifactoryAPI(configs_file_path=os.path.abspath(os.path.join("files", "config.json")))
        self.assertEqual(aapi.configuration.url, "https://alexeybeley.jfrog.io/artifactory/api/")

    def test_system_ping(self):
        aapi = ArtifactoryAPI(configs_file_path=os.path.abspath(os.path.join("files", "config.json")))
        self.assertTrue(aapi.system_ping())

    def test_system_version(self):
        aapi = ArtifactoryAPI(configs_file_path=os.path.abspath(os.path.join("files", "config.json")))
        self.assertEqual(aapi.system_version(), "1.1.1")

    def test_exposed_api(self):
        ArtifactoryAPI(configs_file_path=os.path.abspath(os.path.join("files", "config.json")))
        self.assertEqual(EXPOSED_API, {'configure': 'configure',
                                       'system.version': 'system_version',
                                       'system.ping': 'system_ping'
                                       }
                         )
