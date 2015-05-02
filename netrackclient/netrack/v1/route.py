from netrackclient.netrack.v1 import constants

import collections


_Route = collections.namedtuple("Route", [
    "type",
    "network",
    "via",
    "interface",
    "interface_name",
])


class Route(_Route):

    def __new__(cls, **kwargs):
        kwargs = dict((k, kwargs.get(k)) for k in _Route._fields)
        return super(Route, cls).__new__(cls, **kwargs)


class RouteManager(object):

    def __init__(self, client):
        super(RouteManager, self).__init__()

        self.client = client

    def _url(self, datapath):
        url = "{url_prefix}/datapaths/{datapath}/routes"
        return url.format(url_prefix=constants.URL_PREFIX,
                          datapath=datapath)

    def update(self, datapath, route):
        url = self._url(datapath)
        self.client.put(url, body=[dict(
            network=route.network,
            via=route.via,
            interface_name=route.interface_name,
        )])

    def list(self, datapath):
        url = self._url(datapath)

        response = self.client.get(url)
        return [Route(**route) for route in response.body()]

    def delete(self, datapath, route):
        url = self._url(datapath)
        self.client.delete(url, body=[dict(
            network=route.network,
            via=route.via,
            interface_name=route.interface_name,
        )])
