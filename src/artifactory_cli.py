#!python3
import argparse
import pdb
import sys
from artifactory_api import ArtifactoryAPI, EXPOSED_API


class CLIMenu(object):
    def __init__(self, name):
        self.name = name
        self.func_name = self.name
        self.children = dict()

    def add_menus(self, menus_path, api_func_name):
        pdb.set_trace()
        menus_path.split(".")


class ArtifactoryCLI(object):
    def __init__(self):
        self.name = "ART_OF_CLI"
        self.menu = CLIMenu(self.name)

    def build_menu(self):
        for key, value in EXPOSED_API.items():
            self.menu.add_menus(key, value)


def main():
    art_cli = ArtifactoryCLI()
    art_cli.build_menu()
    art_cli.process_call()


if __name__ == "__main__":
    main()
