from netrackclient.netrack.v1 import constants

import collections
import ipaddress

_Network = collections.namedtuple("Network", [
    "encapsulation",
    "address",
    "broadcast",
    "interface",
    "interface_name",
])


class Network(_Network):

    def __new__(cls, **kwargs):
        kwargs = dict((k, kwargs.get(k)) for k in _Network._fields)
        return super(Network, cls).__new__(cls, **kwargs)


class NetworkManager(object):
    __encapsulation = {
        ipaddress.IPv4Interface: "IPv4",
        ipaddress.IPv6Interface: "IPv6",
    }

    def __init__(self, client):
        super(NetworkManager, self).__init__()

        self.client = client

    def _url(self, datapath, interface):
        url = "{url_prefix}/datapaths/{datapath}/interfaces/{interface}/network"
        return url.format(url_prefix=constants.URL_PREFIX,
                          datapath=datapath,
                          interface=interface)

    def _encapsulation(self, address):
        network = ipaddress.ip_interface(address)
        return self.__encapsulation[network.__class__]

    def update(self, datapath, interface, network):
        url = self._url(datapath, interface)

        # parse address to configure encapsulation
        encapsulation = self._encapsulation(network.address)
        self.client.put(url, body=dict(
            encapsulation=encapsulation,
            address=network.address,
        ))

    def get(self, datapath, interface):
        response = self.client.get(self._url(
            datapath=datapath,
            interface=interface,
        ))

        return Network(**response.body())

    def list(self, datapath):
        url = "{url_prefix}/datapaths/{datapath}/interfaces/networks"
        url = url.format(url_prefix=constants.URL_PREFIX,
                         datapath=datapath)

        response = self.client.get(url)

        interfaces = []
        for interface in response.body():
            interfaces.append(Network(**interface))
        return interfaces

    def delete(self, datapath, interface, network):
        url = self._url(datapath, interface)

        # parse address to configure encapsulation
        encapsulation = self._encapsulation(network.address)
        self.client.put(url, body=dict(
            encapsulation=encapsulation,
            address=network.address,
        ))
