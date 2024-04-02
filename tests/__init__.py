from requests import Response

from sxapi.base import check_response
from sxapi.cli import CliUser
from sxapi.cli.cli import Cli
from sxapi.cli.configuration import Config
from sxapi.cli.parser.main_parser import SxApiMainParser
from sxapi.integrationV2 import IntegrationAPIV2
from sxapi.publicV2 import PublicAPIV2


class ResponseMock(Response):
    def __init__(self, value, status_code, exception=None):
        super().__init__()

        self.exception = exception
        self.value = value
        self.status_code = status_code

    def json(self, **kwargs):
        return self.value


class SxMainTestParser(SxApiMainParser):
    def __init__(self, subparsers=True):
        self.config = Config(configfile="./tests/cli_tests/test-config.conf")

        super().__init__(subparsers=subparsers)


class CliTest(Cli):
    sx_main_parser = SxMainTestParser(subparsers=True)


class APIMock:
    def __init__(self):
        super().__init__()

        self._return_value = None
        self.called_with = []

    def mock_return_value(self, return_value):
        if not isinstance(return_value, ResponseMock):
            raise ValueError("return_value is not of type ResponseMock")

        self._return_value = return_value

    def reset_mock(self):
        self._return_value = []

    @check_response
    def get(self, path, *args, **kwargs):
        self.called_with.append({"path": path, "kwargs": kwargs})
        return self._return_value

    @check_response
    def post(self, path, *args, **kwargs):
        self.called_with.append({"path": path, "kwargs": kwargs})
        return self._return_value

    @check_response
    def put(self, path, *args, **kwargs):
        self.called_with.append({"path": path, "kwargs": kwargs})
        return self._return_value

    @check_response
    def delete(self, path, *args, **kwargs):
        self.called_with.append({"path": path, "kwargs": kwargs})
        return self._return_value


class PublicAPIV2Test(APIMock, PublicAPIV2):
    def __init__(self):
        super().__init__()


class IntegrationAPIV2Test(APIMock, IntegrationAPIV2):
    def __init__(self):
        super().__init__()


class CliUserTest(CliUser):
    def __init__(self):
        super().__init__()

        self.organisation_id = "test_organisation_id"
        self.api_access_token = "test_api_token"
        self.public_v2_api = PublicAPIV2Test()
        self.integration_v2_api = IntegrationAPIV2Test()

    def check_credentials_set(self):
        return True

    def init_user(self, config, args_token, args_keyring, args_orga_id):
        pass
