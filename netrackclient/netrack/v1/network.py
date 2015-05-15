from netrackclient import errors
from netrackclient.netrack.v1 import constants

import collections
import ipaddress

_Network = collections.namedtuple("Network", [
    "encapsulation",
    "address",
    "interface",
    "interface_name",
])


class Network(_Network):

    def __new__(cls, **kwargs):
        kwargs = dict((k, kwargs.get(k)) for k in _Network._fields)
        return super(Network, cls).__new__(cls, **kwargs)


class NetworkManager(object):

    def __init__(self, client):
        super(NetworkManager, self).__init__()

        self.client = client

    def _url(self, datapath, interface):
        url = "{url_prefix}/datapaths/{datapath}/network/interfaces/{interface}"
        return url.format(url_prefix=constants.URL_PREFIX,
                          datapath=datapath,
                          interface=interface)

    def _encapsulation(self, address):
        #TODO: add support of other protocols
        network = ipaddress.ip_interface(address)
        return "ipv{0}".format(network.version)

    def update(self, datapath, interface, network):
        url = self._url(datapath, interface)

        # parse address to configure encapsulation
        encapsulation = self._encapsulation(network.address)

        try:
            self.client.put(url, body=dict(
                encapsulation=encapsulation,
                address=network.address,
            ))
        except errors.BaseError as e:
            raise errors.NetworkError(*e.args)

    def get(self, datapath, interface):

        try:
            response = self.client.get(self._url(
                datapath=datapath,
                interface=interface,
            ))
        except errors.BaseError as e:
            raise errors.NetworkError(*e.args)

        return Network(**response.body())

    def list(self, datapath):
        url = "{url_prefix}/datapaths/{datapath}/network/interfaces"
        url = url.format(url_prefix=constants.URL_PREFIX,
                         datapath=datapath)

        try:
            response = self.client.get(url)
        except errors.BaseErorr as e:
            raise errors.NetworkError(*e.args)

        interfaces = []
        for interface in response.body():
            interfaces.append(Network(**interface))
        return interfaces

    def delete(self, datapath, interface, network):
        url = self._url(datapath, interface)

        # parse address to configure encapsulation
        encapsulation = self._encapsulation(network.address)

        try:
            self.client.delete(url, body=dict(
                encapsulation=encapsulation,
                address=network.address,
            ))
        except errors.BaseError as e:
            raise errors.NetworkError(*e.args)
