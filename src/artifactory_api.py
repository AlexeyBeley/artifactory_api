import json
import os
import pdb


def connection_required(func_base):
    def new_func(args, **kwargs):
        print(ArtifactoryAPI.server_name)
        func_base(args, **kwargs)
    return new_func


class ArtifactoryAPI(object):
    server_name = None

    def __init__(self, configs_file_path=os.path.join(os.path.abspath(__file__), "config.json")):
        with open(configs_file_path) as f:
            configs = json.load(f)
        ArtifactoryAPI.server_name = configs["server_name"]

    @connection_required
    def system_ping(self):
        pdb.set_trace()

