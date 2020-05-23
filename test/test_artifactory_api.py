import os
import sys
import unittest
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "art_cli")))
from artifactory_api import ArtifactoryAPI, EXPOSED_API


class TestArtifactoryAPI(unittest.TestCase):
    def test_init(self):
        art_api = ArtifactoryAPI()
        art_api.configure(file_name=os.path.abspath(os.path.join("files", "config.json")))
        self.assertEqual(art_api.configuration.url, "https://alexeybeley.jfrog.io/artifactory/api/")

    def test_system_ping(self):
        art_api = ArtifactoryAPI()
        art_api.configure(file_name=os.path.abspath(os.path.join("files", "config.json")))
        self.assertTrue(art_api.system_ping())

    def test_system_version(self):
        art_api = ArtifactoryAPI()
        art_api.configure(file_name=os.path.abspath(os.path.join("files", "config.json")))
        self.assertEqual(art_api.system_version(), "1.1.1")

    def test_exposed_api(self):
        ArtifactoryAPI()
        self.assertEqual(EXPOSED_API, {'configure': 'configure',
                                       'package.upload': 'package_upload',
                                       'storage.info': 'storage_get_info',
                                       'system.ping': 'system_ping',
                                       'system.version': 'system_version',
                                       'user.create': 'user_create',
                                       'user.delete': 'user_delete'}
                         )

    def test_exposed_api_cli_parser_flag(self):
        art_api = ArtifactoryAPI()
        art_api.configure(file_name=os.path.abspath(os.path.join("files", "config.json")))
        for func_name in EXPOSED_API.values():
            self.assertIsInstance(getattr(art_api, func_name)(cli_parser=True), argparse.ArgumentParser)


if __name__ == '__main__':
    unittest.main()
