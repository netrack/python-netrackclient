from netrackclient.shell import core
from netrackclient.netrack.v1 import link


class Link(core.BaseCommand):
    name = "link"
    aliases = ["l"]
    help = "network device configuration"

    class Set(core.Command):
        name = "set"
        aliases = ["s"]
        help = "set device attributes"
        arguments = [
            (["dev"],
             dict(metavar="NAME", help="specifies the network device to operate on")),

            (["-a", "--address"],
             dict(metavar="LLADDRESS", help="station address of the interface"))
        ]

        def handle(self, context):
            context.client.network.update(
                # switch identifier (or local port name)
                context.args.datapath,
                # switch port name
                context.args.device,
                # link configuration
                link.Link(
                    encapsulation="ETHERNET-II#802.3",
                    address=context.args.address,
                ))

    class Del(core.Command):
        name = "del"
        aliases = ["delete", "d"]
        help = "delete device attributes"
        arguments = [
            (["address"],
             dict(metavar="ADDRESS",
                  help="station address of the interface",
                  nargs="?")),

            (["-d", "--device"],
             dict(metavar="NAME",
                  help="network device to operate on",
                  required=True)),
        ]

        def handle(self, context):
            context.client.link.delete(
                context.args.datapath,
                context.args.device)

    class Show(core.Command):
        name = "show"
        aliases = ["list", "lst", "sh", "ls", "l"]
        help = "look at device attributes"
        arguments = [
            (["-d", "--device"],
             dict(metavar="NAME",
                  help="network device to operate on")),
        ]

        def render(self, link):
            print("{index}: {interface}: <BROADCAST,UP,LOWER_UP>".format(
                index=link.interface,
                interface=link.interface_name))

            if link.address:
                print("    link/{proto} {addr} brd ffff.ffff.ffff".format(
                    proto=link.encapsulation.lower(),
                    addr=link.address))

        def handle(self, context):
            links_fetcher = context.client.link.list
            args = (context.args.datapath,)

            if context.args.device:
                liks_fetcher = context.client.link.get
                args = (context.args.datapath, context.args.device)

            links = links_fetcher(*args)

            # sort devices by interface number
            predicate = lambda x: x.interface
            links = sorted(links, key=predicate)

            list(map(self.render, links))
