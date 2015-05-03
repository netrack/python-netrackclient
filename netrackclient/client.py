import sys
import json
import importlib
import traceback

from netrackclient import broker
from netrackclient import errors


class HTTPClient(object):

    def __init__(self, *args, **kwargs):
        super(HTTPClient, self).__init__()

        self._broker = broker.RequestBroker()
        self.service_url = kwargs.get("service_url")

    def _request(self):
        request = self._broker.http_request()
        request.add_header("Content-Type", "application/json")
        request.add_header("Accept", "application/json")
        return request

    def get(self, uri, **kwargs):
        request = self._request()
        url = self.service_url + uri
        return request.get(url, **kwargs)

    def put(self, uri, body, **kwargs):
        request = self._request()
        url = self.service_url + uri
        body = json.dumps(body)
        return request.put(url, body, **kwargs)

    def delete(self, uri, body, **kwargs):
        request = self._request()
        url = self.service_url + uri
        body = json.dumps(body)
        return request.delete(url, body, **kwargs)


__version_map = {
    "1": "netrackclient.netrack.v1.client:Client",
}


def get_client_class(version):
    try:
        class_path = __version_map[str(version)]
        module_path, _, class_name = class_path.rpartition(":")
        module = importlib.import_module(module_path)
        return getattr(module, class_name)

    except AttributeError:
        msg = "Class {class_name} cannot be found ({exception}))".format(
            class_name=class_name,
            exception=traceback.format_exception(*sys.exc_info()))
        raise errors.VersionError(msg)

    except (KeyError, ValueError):
        msg = "Invalid client version '{version}'. must be one of: ".format(
            version=version)
        msg += "{versions}".format(versions=", ".join(__version_map.keys()))
        raise errors.VersionError(msg)


def Client(version="1", *args, **kwargs):
    client_class = get_client_class(version)
    return client_class(*args, **kwargs)
