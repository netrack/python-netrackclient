from netrackclient.shell import core


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
             dict(metavar="ROUTE", help="destination route")),

            (["-via", "--via"],
             dict(metavar="ADDRESS", help="the address of nexthop router")),

            (["-d", "--device"],
             dict(metavar="NAME", help="the output device name")),
        ]

        def handle(self, context):
            pass

    class Del(core.Command):
        name = "del"
        aliases = ["delete", "d"]
        help = "delete route"

        def handle(self, context):
            pass

    class Show(core.Command):
        name = "show"
        aliases = ["list", "sh", "ls", "l"]
        help = "look at routing table"

        def handle(self, context):
            pass
