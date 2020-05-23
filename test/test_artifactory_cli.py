import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "art_cli")))
from artifactory_cli import main, CLIMenu


class TestCLIMenu(unittest.TestCase):
    #@unittest.skip("todo:")
    def test_split_full_call_path(self):
        cli_menu = CLIMenu("prog_name")
        cli_menu.add_submenus("1.2.3.4", "1234")
        cli_menu.add_submenus("1.2.3", "123")
        cli_menu.add_submenus("1", "1")
        cli_menu.add_submenus("2", "2")
        cli_menu.add_submenus("3.1", "31")
        cli_menu.add_submenus("3.2", "32")

        call_path, func_name, args = cli_menu.split_full_call_path(["prog_name", "1", "2", "3", "4", "arg1", "arg2", "arg3"])
        self.assertEqual([call_path, func_name, args], [["prog_name", "1", "2", "3", "4"], "1234", ["arg1", "arg2", "arg3"]])

        call_path, func_name, args = cli_menu.split_full_call_path(["prog_name", "1", "arg1", "arg2"])
        self.assertEqual([call_path, func_name, args], [["prog_name", "1"], "1", ["arg1", "arg2"]])

        call_path, func_name, args = cli_menu.split_full_call_path(["prog_name", "3", "3", "arg1", "arg2"])
        self.assertEqual([call_path, func_name, args], [["prog_name", "3"], None, ["3", "arg1", "arg2"]])

class TestArtifactoryCLI(unittest.TestCase):
    #@unittest.skip("todo:")
    def test_main(self):
        testargs = ["ART_OF_CLI", "configure", "-f", os.path.abspath(os.path.join("files", "config.json"))]
        with patch.object(sys, 'argv', testargs):
           main()
        #aapi = ArtifactoryCLI(configs_file_path=os.path.abspath(os.path.join("files", "config.json")))
        #self.assertEqual(aapi.configuration.url, "https://alexeybeley.jfrog.io/artifactory/api/")

    @unittest.skip("todo:")
    def test_system_wrong(self):
        testargs = ["art_cli", "system", "-f", os.path.abspath(os.path.join("files", "config.json"))]
        with patch.object(sys, 'argv', testargs):
           main()
        #aapi = ArtifactoryCLI(configs_file_path=os.path.abspath(os.path.join("files", "config.json")))
        #self.assertEqual(aapi.configuration.url, "https://alexeybeley.jfrog.io/artifactory/api/")

    @unittest.skip("todo:")
    def test_system_ping(self):
        testargs = ["art_cli", "system", "ping"]
        with patch.object(sys, 'argv', testargs):
           main()
        #aapi = ArtifactoryCLI(configs_file_path=os.path.abspath(os.path.join("files", "config.json")))
        #self.assertEqual(aapi.configuration.url, "https://alexeybeley.jfrog.io/artifactory/api/")


if __name__ == '__main__':
    unittest.main()
