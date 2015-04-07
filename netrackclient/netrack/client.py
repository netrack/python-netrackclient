from netrackclient.netrack.v1 import address
from netrackclient.netrack.v1 import link
from netrackclient.netrack.v1 import neigh


class Client(object):

    def __init__(self):
        super(Client, self).__init__()

        self.address = address.AddressManager(self)
        self.link = link.LinkManager(self)
        self.neigh = neigh.NeighManager(self)
