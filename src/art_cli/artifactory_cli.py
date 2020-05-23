#!python3
import sys
from artifactory_api import ArtifactoryAPI, EXPOSED_API
import pdb
import argparse


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

    def split_full_call_path(self, lst_path):
        if self.name != lst_path[0]:
            raise RuntimeError("Invalid submenu call '{}, expected '{}'".format(lst_path[0], self.name))

        if len(lst_path) == 1 or lst_path[1] not in self.children:
            return [self.name], self.func_name, lst_path[1:]

        children_submenus, func_name, args_split = self.children[lst_path[1]].split_full_call_path(lst_path[1:])
        children_submenus.insert(0, self.name)
        return children_submenus, func_name, args_split

    def generate_usage(self, submenus, function_name, function_args):
        help_message = 'please run "ART_CLI --USAGE" for all options.'
        if len(submenus) == 1:
            parser = argparse.ArgumentParser(add_help=False)
            parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                                help=help_message)
            parser.add_argument('--USAGE', action='store_true')

            args = parser.parse_args(sys.argv[1:])
            if args.USAGE is True:
                self.print_all_menus_usage([])
            else:
                print(help_message)

            return

        pdb.set_trace()
        usage = ""
        print(usage)

    def print_all_menus_usage(self, lst_path):
        str_ret = ""
        lst_path.append(self.name)

        for child_name, child in self.children.items():
            if child.func_name is not None:
                func_obj = getattr(ArtifactoryAPI(), child.func_name)
                parser = func_obj(cli_parser=True)
                print('Available options for "{} {}":'.format(" ".join(lst_path), child_name))
                parser.print_usage()
            else:
                child.print_all_menus_usage(lst_path)
                lst_path.pop(-1)

        return str_ret

class ArtifactoryCLI(object):
    ART_API = ArtifactoryAPI()

    def __init__(self):
        self.name = "ART_OF_CLI"
        self.menu = CLIMenu(self.name)

    def build_menu(self):
        for key, value in EXPOSED_API.items():
            self.menu.add_submenus(key, value)

    def process_call(self):
        submenus, function_name, function_args = self.menu.split_full_call_path(sys.argv)
        if not function_name:
            self.menu.generate_usage(submenus, function_name, function_args)
            return
        func_obj = getattr(self.ART_API, function_name)
        parser = func_obj(cli_parser=True)

        args = parser.parse_args(sys.argv[len(submenus):])
        return func_obj(**vars(args))


def main():
    art_cli = ArtifactoryCLI()
    art_cli.build_menu()
    art_cli.process_call()
    return True


if __name__ == "__main__":
    main()
