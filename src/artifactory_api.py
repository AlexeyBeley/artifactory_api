import json
import os
import pdb
import requests
from urllib.parse import urljoin
import time
from functools import wraps


#region Static functions and Consts


SESSION_RETRY_COUNT = 3
SESSION_RETRY_SLEEP_INTERVAL = 5
EXPOSED_API = {}


def connection_required(func_base):
    @wraps(func_base)
    def new_func(args, **kwargs):
        try:
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


#endregion


class APICallError(RuntimeError):
    pass


class NotConnectedError(RuntimeError):
    pass


class APIImplementationOverrideError(RuntimeError):
    pass


class APIConfiguration(object):
    def __init__(self, configs_file_path):
        with open(configs_file_path) as f:
            configs = json.load(f)
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

    def __init__(self, configs_file_path=os.path.join(os.path.abspath(__file__), "config.json")):
        ArtifactoryAPI.configuration = APIConfiguration(configs_file_path)

    @expose_api("system.version")
    @connection_required
    def system_version(self):
        return "1.1.1"

    @expose_api("system.ping")
    @connection_required
    def system_ping(self):
        """
        Perform API call to the Artifactory server.
        '/system/ping'

        :return: True if ping succeeded False else
        """
        try:
            ArtifactoryAPI.execute("system/ping")
            return True
        except ConnectionError:
            raise
        except Exception as e:
            print("Error received executing system_ping: {}".format(repr(e)))
        return False

    @staticmethod
    def connect():
        ArtifactoryAPI.session = requests.Session()
        ArtifactoryAPI.session.auth = (ArtifactoryAPI.configuration.username, ArtifactoryAPI.configuration.password)

    @staticmethod
    @retry("Api called failed.", (APICallError, requests.HTTPError, requests.ConnectionError))
    def execute(command, retry_on_error_code=True):
        url = urljoin(ArtifactoryAPI.configuration.url, command)
        for count in range(ArtifactoryAPI.configuration.retry_count):
            try:
                ret = ArtifactoryAPI.session.get(url)
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





