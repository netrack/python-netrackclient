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
            (["device"],
             dict(metavar="NAME",
                  help="specifies the network device to operate on")),

            (["-a", "--address"],
             dict(metavar="LLADDRESS",
                  help="station address of the interface"))
        ]

        def handle(self, context):
            context.client.link.update(
                # switch identifier (or local port name)
                context.args.datapath,
                # switch port name
                context.args.device,
                # link configuration
                link.Link(
                    encapsulation="ieee-802.3",
                    address=context.args.address,
                ))

    class Del(core.BaseCommand):
        name = "del"
        aliases = ["delete", "d"]
        help = "delete device attributes"
        arguments = [
            (["device"],
             dict(metavar="NAME",
                  help="network device to operate on",
                  nargs="?")),
        ]

        def handle(self, context):
            context.client.link.delete(
                context.args.datapath,
                context.args.device)

    class Show(core.BaseCommand):
        name = "show"
        aliases = ["list", "lst", "sh", "ls", "l"]
        help = "look at device attributes"
        arguments = [
            (["-d", "--device"],
             dict(metavar="NAME",
                  help="network device to operate on")),
        ]

        def render(self, link):
            print("{index}: {interface}: <{config}> state {state} {features}".format(
                index=link.interface,
                interface=link.interface_name,
                config=link.config or "UNKNOWN",
                state=link.state or "UNKNOWN",
                features=link.features or ""))

            if link.address:
                print("    link/{proto} {addr} brd ffff.ffff.ffff".format(
                    proto=link.encapsulation.lower(),
                    addr=link.address))

        def handle(self, context):
            links_fetcher = context.client.link.list

            args = (context.args.datapath,)
            make_fetcher = lambda func: lambda *args: [func(*args)]

            if context.args.device:
                links_fetcher = make_fetcher(context.client.link.get)
                args = (context.args.datapath, context.args.device)

            links = links_fetcher(*args)

            # sort devices by interface number
            predicate = lambda x: x.interface
            links = sorted(links, key=predicate)

            list(map(self.render, links))

    class Module(core.BaseCommand):
        name = "module"
        aliases = ["mod"]
        help = "configure link modules"
        arguments = [
            (["module"],
             dict(metavar="NAME",
                  help="link module name",
                  nargs="?")),
        ]

        class Show(core.BaseCommand):
            name = "show"
            help = "look at link modules"

            def render(self, module):
                print("{name} <{state}> {desc}".format(
                    name=module.name,
                    state=module.state,
                    desc=module.description))

            def handle(self, context):
                modules_fetcher = context.client.linkmod.list

                args = (context.args.datapath,)
                make_fetcher = lambda func: lambda *args: [func(*args)]

                if context.args.module:
                    modules_fetcher = make_fetcher(context.client.link.get)
                    args = (context.args.datapath, context.args.module)

                modules = modules_fetcher(*args)
                list(map(self.render, modules))

        class On(core.BaseCommand):
            name = "on"
            help = "turn on specified link module"

            def handle(self, context):
                context.client.linkmod.enable(
                    datapath=context.args.datapath,
                    module=context.args.module)

        class Off(core.BaseCommand):
            name = "off"
            help = "turn off specified link module"

            def handle(self, context):
                context.client.linkmod.disable(
                    datapath=context.args.datapath,
                    module=context.args.module)
