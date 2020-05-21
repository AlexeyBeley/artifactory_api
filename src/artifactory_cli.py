#!python3
import argparse
import pdb
import sys
from artifactory_api import ArtifactoryAPI, EXPOSED_API


class CLIMenu(object):
    def __init__(self, name):
        self.name = name


class ArtifactoryCLI(object):
    def __init__(self):
        pdb.set_trace()


def main():
   print(sys.argv)
   art_cli = ArtifactoryCLI()
   art_cli.build_menu(EXPOSED_API)
   art_cli


if __name__ == "__main__":
    main()
