from netrackclient.netrack.v1 import constants

import collections

_Link = collections.namedtuple("Link", [
    "encapsulation",
    "address",
    "interface",
    "interface_name",
])


class Link(_Link):

    def __new__(cls, **kwargs):
        kwargs = dict((k, kwargs.get(k)) for k in _Link._fields)
        return super(Link, cls).__new__(cls, **kwargs)


class LinkManager(object):

    def __init__(self, client):
        super(LinkManager, self).__init__()

        self.client = client

    def _url(self, datapath, interface):
        url = "{url_prefix}/datapaths/{datapath}/interfaces/{interface}/link"
        return url.format(url_prefix=constants.URL_PREFIX,
                          datapath=datapath,
                          interface=interface)

    def update(self, datapath, interface, link):
        url = self._url(datapath, interface)

        self.client.put(url, body=dict(
            encapsulation=link.encapsulation,
            address=link.address,
        ))

    def get(self, datapath, interface):
        response = self.client.get(self._url(
            datapath=datapath,
            interface=interface,
        ))

        return Link(**response.body())

    def list(self, datapath):
        url = "{url_prefix}/datapaths/{datapath}/interfaces/links"
        url = url.format(url_prefix=constants.URL_PREFIX,
                         datapath=datapath)

        response = self.client.get(url)

        interfaces = []
        for interface in response.body():
            interfaces.append(Link(**interface))
        return interfaces

    def delete(self, datapath, interface):
        self.client.delete(self._url(
            datapath=datapath,
            interface=interface,
        ))
