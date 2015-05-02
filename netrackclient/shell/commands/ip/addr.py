from netrackclient.shell import core
from netrackclient.netrack.v1 import network
from netrackclient.netrack.v1 import link


class Addr(core.BaseCommand):
    name = "addr"
    aliases = ["address", "a"]
    help = "protocol address management"

    class Add(core.Command):
        name = "add"
        aliases = ["a"]
        help = "add new protocol address"
        arguments = [
            (["address"],
             dict(metavar="ADDRESS",
                  help="address of the interface",
                  nargs="?")),

            (["-d", "--device"],
             dict(metavar="NAME",
                  help="name of the device to which we add the address",
                  required=True)),
        ]

        def handle(self, context):
            context.client.network.update(
                # switch identifier (or local port name)
                context.args.datapath,
                # switch port name
                context.args.device,
                # network configuration
                network.Network(address=context.args.address))

    class Del(core.Command):
        name = "del"
        aliases = ["delete", "d"]
        help = "delete protocol address"
        arguments = [
            (["address"],
             dict(metavar="ADDRESS",
                  help="address of the interface",
                  nargs="?")),

            (["-d", "--device"],
             dict(metavar="NAME",
                  help="name of the device to which we add the address",
                  required=True)),
        ]

        def handle(self, context):
            context.client.network.delete(
                context.args.datapath,
                context.args.device,
                network.Network(address=context.args.address))

    class Show(core.Command):
        name = "show"
        aliases = ["list", "lst", "sh", "ls", "l"]
        help = "look at protocol addresses"
        arguments = [
            (["-d", "--device"],
             dict(metavar="NAME",
                  help="name of the device to which we add the address")),
        ]

        def render(self, link, network):
            print("{index}: {interface}: <BROADCAST,UP,LOWER_UP>".format(
                index=link.interface,
                interface=link.interface_name))

            if link.address:
                print("    link/{proto} {addr} brd ffff.ffff.ffff".format(
                    proto=link.encapsulation.lower(),
                    addr=link.address))

            if network.address:
                print("    inet/{proto} {addr} brd {bcast} scope global {interface}".format(
                    proto=network.encapsulation.lower(),
                    addr=network.address,
                    bcast=network.broadcast,
                    interface=link.interface_name))

        def handle(self, context):
            networks_fetcher = context.client.network.list
            links_fetcher = context.client.link.list

            args = (context.args.datapath,)

            if context.args.device:
                networks_fetcher = context.client.network.get
                links_fetcher = context.client.link.get
                args = (context.args.datapath, context.args.device)

            networks = networks_fetcher(*args)
            links = links_fetcher(*args)

            # sort devices by interface number
            predicate = lambda x: x.interface
            networks = sorted(networks, key=predicate)
            links = sorted(links, key=predicate)

            # render links and networks
            list(map(lambda args: self.render(*args), zip(links, networks)))