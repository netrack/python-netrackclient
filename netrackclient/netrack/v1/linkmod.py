from netrackclient import errors
from netrackclient.netrack.v1 import constants

import collections


_Module = collections.namedtuple("Module", [
    "name",
    "description",
    "state",
])


class Module(_Module):

    def __new__(cls, **kwargs):
        kwargs = dict((k, kwargs.get(k)) for k in _Module._fields)
        return super(Module, cls).__new__(cls, **kwargs)


class LinkModuleManager(object):

    def __init__(self, client):
        super(LinkModuleManager, self).__init__()

        self.client = client

    def _url(self, datapath, module):
        url = "{url_prefix}/datapaths/{datapath}/link/mechanisms".format(
                datapath=datapath,
                url_prefix=constants.URL_PREFIX)

        if module:
            url += "/{module}".format(module=module)

        return url

    def _check_module(self, module):
        if not module:
            raise errors.LinkError({"error": "not a link module"})

    def get(self, datapath, module):
        self._check_module(module)
        url = self._url(datapath, module)

        try:
            response = self.client.get(url)
        except errors.BaseError as e:
            raise errors.LinkError(*e.args)

        return Module(**response.body())

    def list(self, datapath):
        url = self._url(datapath, None)

        try:
            response = self.client.get(url)
        except errors.BaseError as e:
            raise errors.LinkError(*e.args)

        return [Module(**module) for module in response.body()]

    def enable(self, datapath, module):
        self._check_module(module)
        url = self._url(datapath, module) + "/enable"

        try:
            self.client.put(url, body=None)
        except errors.BaseError as e:
            raise errors.LinkError(*e.args)

    def disable(self, datapath, module):
        self._check_module(module)
        url = self._url(datapath, module) + "/disable"

        try:
            self.client.put(url, body=None)
        except errors.BaseError as e:
            raise errors.LinkError(*e.args)
