import os
import pdb
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from artifactory_cli import ArtifactoryCLI, main

class TestArtifactoryCLI(unittest.TestCase):
    def test_main(self):
        testargs = ["prog", "configure", "-f", os.path.abspath(os.path.join("files", "config.json"))]
        with patch.object(sys, 'argv', testargs):
           main()
        aapi = ArtifactoryCLI(configs_file_path=os.path.abspath(os.path.join("files", "config.json")))
        self.assertEqual(aapi.configuration.url, "https://alexeybeley.jfrog.io/artifactory/api/")

