import json
import os
import pdb
import requests
from urllib.parse import urljoin
import time
from functools import wraps
import argparse
from enum import Enum

# region Consts
SESSION_RETRY_COUNT = 3
SESSION_RETRY_SLEEP_INTERVAL = 5
EXPOSED_API = {}
# endregion

# region Decorators


def connection_required(func_base):
    @wraps(func_base)
    def new_func(args, **kwargs):
        try:
            ArtifactoryAPI().configure()
            return func_base(args, **kwargs)
        except ConnectionError:
            ArtifactoryAPI.connect()
            return func_base(args, **kwargs)

    return new_func


def retry(log_message, tuple_exceptions):
    def wrap(func_base):
        def func_new(args, **kwargs):
            for i in range(ArtifactoryAPI.configuration.retry_count):
                try:
                    return func_base(args, **kwargs)
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
        def func_new(args, **kwargs):
            return func_base(args, **kwargs)

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
    CONFIGS_PATH = os.path.join(os.path.dirname(__file__), "_private", "configs.json")

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

        if file_name != ArtifactoryAPI.CONFIGS_PATH:
            with open(ArtifactoryAPI.CONFIGS_PATH, "w") as f:
                f.write(json.dumps(configs))

        ArtifactoryAPI.configuration = APIConfiguration(configs)

    @expose_api("system.version")
    @connection_required
    def system_version(self, cli_parser=False):
        if cli_parser:
            return self.default_parser

        return "1.1.1"

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
            ArtifactoryAPI.execute("system/ping")
            print("OK")
            return True
        except ConnectionError:
            raise
        except Exception as e:
            print("Error received executing system_ping: {}".format(repr(e)))
        return False

    @expose_api("user.delete")
    @connection_required
    def user_delete(self, cli_parser=False):
        if cli_parser:
            return self.name_parser()

        raise NotImplementedError("the same as below")

    @expose_api("user.create")
    @connection_required
    def user_create(self, cli_parser=False, file_name=None):
        if cli_parser:
            return self.file_name_parser()

        ArtifactoryAPI.execute("system/ping")

        requests.put('https://httpbin.org/put', data={'key': 'value'})
        #
        return True
        pdb.set_trace()
        print("Press ^+D to submit the valid JSON input")
        complete_inout = sys.stdin.read()
        pdb.set_trace()
        print(complete_inout)
        {"1": "2",
         "3": "4"
         }

    @expose_api("storage.info")
    @connection_required
    def storage_get_info(self, cli_parser=False):
        if cli_parser:
            return self.default_parser

        raise NotImplementedError("GET /api/storageinfo")

    @expose_api("package.upload")
    @connection_required
    def package_upload(self, cli_parser=False):
        if cli_parser:
            return self.dir_name_parser()

        raise NotImplementedError("upload package")

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

                if ret.status_code != 200:
                    if retry_on_error_code:
                        raise APICallError("Error code: {}, reason: {}".format(ret.status_code, ret.reason))
                    else:
                        print("Error when calling {} code: {}, reason: {}".format(url, ret.status_code, ret.reason))

                return ret
            except AttributeError as e:
                if "'NoneType' object has no attribute 'get'" in repr(e):
                    raise ConnectionError("Not connected")
                raise
            except (requests.HTTPError, requests.ConnectionError):
                time.sleep(ArtifactoryAPI.configuration.retry_sleep_interval)

    class APIMethods(Enum):
        GET = 0
        PUT = 1
        DELETE = 2
