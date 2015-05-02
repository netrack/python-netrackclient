from netrackclient.shell import core

from netrackclient.shell.commands.ip import addr as _addr
from netrackclient.shell.commands.ip import link as _link
from netrackclient.shell.commands.ip import route as _route

class IP(core.BaseCommand):
    name = "ip"
    help = "show/manipulate routing and devices"

    Addr = _addr.Addr
    Link = _link.Link
    Route = _route.Route
