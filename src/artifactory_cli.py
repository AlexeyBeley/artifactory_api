#!python3
import argparse
import pdb
import sys
from artifactory_api import ArtifactoryAPI, EXPOSED_API


class CLIMenu(object):

    def __init__(self, name):
        self.name = name
        self.func_name = None
        self.children = dict()

    def add_submenus(self, menus_path, api_func_name):
        """

        :param menus_path: dot separated string of submenus without my own name
        :param api_func_name: ArtifactoryAPI real function name
        :return: None
        """

        submenu = self
        for submenu_name in menus_path.split("."):
            submenu = submenu.add_submenu(submenu_name)
        submenu.func_name = api_func_name

    def add_submenu(self, name):
        if name not in self.children:
            self.children[name] = CLIMenu(name)

        return self.children.get(name)


class ArtifactoryCLI(object):
    ART_API = ArtifactoryAPI()

    def __init__(self):
        self.name = "ART_OF_CLI"
        self.menu = CLIMenu(self.name)

    def build_menu(self):
        for key, value in EXPOSED_API.items():
            self.menu.add_submenus(key, value)

    def process_call(self):
        submenus, function_name, function_args = self.split_to_submenus_function_and_args()
        if not function_name:
            self.menu.generate_usage(submenus, function_name, function_args)
            return
        func_obj = getattr(self.ART_API, function_name)
        parser = func_obj(cli_parser=True)
        args = parser.parse_args(sys.argv[len(submenus):])
        return func_obj(args)


def main():
    art_cli = ArtifactoryCLI()
    art_cli.build_menu()
    art_cli.process_call()


if __name__ == "__main__":
    main()
