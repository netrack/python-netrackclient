from netrackclient.shell import core
from netrackclient.netrack.v1 import route


class Route(core.BaseCommand):
    name = "route"
    aliases = ["ro", "r"]
    help = "routing table management"

    class Add(core.Command):
        name = "add"
        aliases = ["a"]
        help = "add new route"
        arguments = [
            (["route"],
             dict(metavar="ROUTE",
                  help="destination route")),

            (["-via", "--via"],
             dict(metavar="ADDRESS",
                  help="the address of nexthop router",
                  required=True)),

            (["-d", "--device"],
             dict(metavar="NAME",
                  help="the output device name",
                  required=True)),
        ]

        def handle(self, context):
            context.client.route.update(
                # switch identifier (or local port name)
                context.args.datapath,
                # route configuration
                route.Route(
                    network=context.args.route,
                    via=context.args.via,
                    interface_name=context.args.device))

    class Del(core.Command):
        name = "del"
        aliases = ["delete", "d"]
        help = "delete route"
        arguments = [
            (["route"],
             dict(metavar="ROUTE",
                  help="destination route")),

            (["-via", "--via"],
             dict(metavar="ADDRESS",
                  help="the address of nexthop router",
                  required=True)),

            (["-d", "--device"],
             dict(metavar="NAME",
                  help="the output device name",
                  required=True)),
        ]

        def handle(self, context):
            context.client.route.delete(
                context.args.datapath,
                route.Route(
                    network=context.args.route,
                    via=context.args.via,
                    interface_name=context.args.device))

    class Show(core.Command):
        name = "show"
        aliases = ["list", "sh", "ls", "l"]
        help = "look at routing table"

        def render(self, route):
            via = " via {0}".format(route.via) if route.via else ""

            print("{network}{via} dev {interface} proto {type}".format(
                network=route.network,
                via=via,
                interface=route.interface_name,
                type=route.type))

        def handle(self, context):
            routes = context.client.route.list(
                context.args.datapath)

            list(map(self.render, routes))
