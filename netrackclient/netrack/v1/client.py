from netrackclient import client
from netrackclient.netrack.v1 import link
from netrackclient.netrack.v1 import route
from netrackclient.netrack.v1 import network
from netrackclient.netrack.v1 import linkmod
from netrackclient.netrack.v1 import netmod


class Client(client.HTTPClient):

    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)

        self.link = link.LinkManager(self)
        self.network = network.NetworkManager(self)
        self.route = route.RouteManager(self)
        self.linkmod = linkmod.LinkModuleManager(self)
        self.netmod = netmod.NetworkModuleManager(self)
