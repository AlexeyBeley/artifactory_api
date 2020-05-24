import json
import os
import requests
from urllib.parse import urljoin
import time
from functools import wraps
import argparse
from enum import Enum
import pprint

# region Consts
SESSION_RETRY_COUNT = 3
SESSION_RETRY_SLEEP_INTERVAL = 5
EXPOSED_API = {}
# endregion

# region Decorators


def connection_required(func_base):
    @wraps(func_base)
    def new_func(*args, **kwargs):
        try:
            ArtifactoryAPI().configure()
            return func_base(*args, **kwargs)
        except ConnectionError:
            ArtifactoryAPI.connect()
            return func_base(*args, **kwargs)

    return new_func


def retry(log_message, tuple_exceptions):
    def wrap(func_base):
        def func_new(*args, **kwargs):
            for i in range(ArtifactoryAPI.configuration.retry_count):
                try:
                    return func_base(*args, **kwargs)
                except tuple_exceptions as e:
                    print("{} Reason: {}, retrying in {}".format(log_message, repr(e), ArtifactoryAPI.configuration.retry_sleep_interval))
                    time.sleep(ArtifactoryAPI.configuration.retry_sleep_interval)
        return func_new
    return wrap


def expose_api(api_path):
    def wrap(func_base):
        if api_path in EXPOSED_API:
            raise APIImplementationOverrideError("API path exists: {}".format(api_path))

        EXPOSED_API[api_path] = func_base.__name__

        @wraps(func_base)
        def func_new(*args, **kwargs):
            return func_base(*args, **kwargs)

        return func_new
    return wrap
# endregion

# region Exceptions


class APICallError(RuntimeError):
    pass


class NotConnectedError(RuntimeError):
    pass


class APIImplementationOverrideError(RuntimeError):
    pass

# endregion

class APIConfiguration(object):
    def __init__(self, configs):
        self.username = configs.get("username")
        self.password = configs.get("password")
        self.url = "{}://{}/api/".format(configs["protocol"], configs["server_name"])

        self.retry_count = configs.get("retry_count")
        self.retry_count = SESSION_RETRY_COUNT if self.retry_count is None else self.retry_count
        self.retry_sleep_interval = configs.get("retry_sleep_interval")  # seconds
        self.retry_sleep_interval = SESSION_RETRY_SLEEP_INTERVAL if self.retry_sleep_interval is None else self.retry_sleep_interval


class ArtifactoryAPI(object):
    configuration = None
    session = None
    CONFIGS_PATH = os.path.join("/tmp", "configs.json")

    def __init__(self):
        self.default_parser = argparse.ArgumentParser()

    @staticmethod
    def file_name_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument('-f',
                            '--file_name',
                            action='store',
                            type=str,
                            metavar='FILE_NAME')
        return parser

    @staticmethod
    def dir_name_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument('-d',
                            '--dir_name',
                            action='store',
                            type=str,
                            metavar='DIR_NAME')
        return parser

    @staticmethod
    def name_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument('-n',
                            '--name',
                            action='store',
                            type=str,
                            metavar='NAME')
        return parser

    @expose_api("configure")
    def configure(self, cli_parser=False, file_name=None):
        """

        :param cli_parser:
        :param file_name:
        :return:
        """

        if cli_parser:
            return ArtifactoryAPI.file_name_parser()

        if file_name is None:
            file_name = ArtifactoryAPI.CONFIGS_PATH

        with open(file_name) as f:
            configs = json.load(f)

        try:
            if file_name != ArtifactoryAPI.CONFIGS_PATH:
              with open(ArtifactoryAPI.CONFIGS_PATH, "w") as f:
                    f.write(json.dumps(configs))
        except FileNotFoundError:
            print("Valid Configuration file needed")

        ArtifactoryAPI.configuration = APIConfiguration(configs)

    @expose_api("system.version")
    @connection_required
    def system_version(self, cli_parser=False):
        if cli_parser:
            return self.default_parser
        ret = ArtifactoryAPI.execute("system/version", ArtifactoryAPI.APIMethods.GET)

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(json.loads(ret.text))
        return "ok"

    @expose_api("system.ping")
    @connection_required
    def system_ping(self, cli_parser=False):
        """
        Perform API call to the Artifactory server.
        '/system/ping'

        :return: True if ping succeeded False else
        """
        if cli_parser:
            return self.default_parser

        try:
            ArtifactoryAPI.execute("system/ping", ArtifactoryAPI.APIMethods.GET)
            print("OK")
            return True
        except ConnectionError:
            raise
        except Exception as e:
            print("Error received executing system_ping: {}".format(repr(e)))
        return False

    @expose_api("user.delete")
    @connection_required
    def user_delete(self, cli_parser=False, name=None):
        if cli_parser:
            return self.name_parser()

        ret = ArtifactoryAPI.execute("security/users/{}".format(name), ArtifactoryAPI.APIMethods.DELETE,
                                     retry_on_error_code=False)

        if ret.status_code == 200:
            print("OK")
            return True

        return False

    @expose_api("user.create")
    @connection_required
    def user_create(self, cli_parser=False, file_name=None):
        if cli_parser:
            return self.file_name_parser()

        with open(file_name) as f:
            user = json.load(f)
            ret = ArtifactoryAPI.execute("security/users/{}".format(user["name"]), ArtifactoryAPI.APIMethods.PUT,
                                   data=json.dumps(user), retry_on_error_code=False)

        if ret.status_code == 201:
            print("OK")
            return True

        return False
        # todo: add an option to put data interactively
        print("Press ^+D to submit the valid JSON input")
        complete_inout = sys.stdin.read()
        print(complete_inout)

    @expose_api("storage.info")
    @connection_required
    def storage_get_info(self, cli_parser=False):
        if cli_parser:
            return self.default_parser

        ret = ArtifactoryAPI.execute("storageinfo", ArtifactoryAPI.APIMethods.GET)

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(json.loads(ret.text))
        return "ok"

    @expose_api("package.upload")
    @connection_required
    def package_upload(self, cli_parser=False):
        if cli_parser:
            return self.dir_name_parser()

        raise NotImplementedError("Upload package should be part of the CLI")

    @staticmethod
    def connect():
        ArtifactoryAPI.session = requests.Session()
        ArtifactoryAPI.session.auth = (ArtifactoryAPI.configuration.username, ArtifactoryAPI.configuration.password)

    @staticmethod
    @retry("Api called failed.", (APICallError, requests.HTTPError, requests.ConnectionError))
    def execute(command, method, retry_on_error_code=True, data=None):
        url = urljoin(ArtifactoryAPI.configuration.url, command)
        for count in range(ArtifactoryAPI.configuration.retry_count):
            try:
                if method == ArtifactoryAPI.APIMethods.GET:
                    ret = ArtifactoryAPI.session.get(url)
                elif method == ArtifactoryAPI.APIMethods.PUT:
                    ret = ArtifactoryAPI.session.put(url, data=data)
                elif method == ArtifactoryAPI.APIMethods.DELETE:
                    ret = ArtifactoryAPI.session.delete(url)
                else:
                    raise RuntimeError("Unexpected method {}, method should be one of {}".format(method, ArtifactoryAPI.APIMethods._member_names_))

                if ret.status_code not in [200, 201]:
                    if retry_on_error_code:
                        raise APICallError("Error code: {}, reason: {}".format(ret.status_code, ret.reason))
                    else:
                        print("Error when calling {} code: {}, reason: {}".format(url, ret.status_code, ret.reason))
                        content = ret.__dict__.get("_content")
                        if content:
                            print(content)
                return ret
            except AttributeError as e:
                if "'NoneType' object has no attribute " in repr(e):
                    raise ConnectionError("Not connected")
                raise
            except (requests.HTTPError, requests.ConnectionError):
                time.sleep(ArtifactoryAPI.configuration.retry_sleep_interval)

    class APIMethods(Enum):
        GET = 0
        PUT = 1
        DELETE = 2
