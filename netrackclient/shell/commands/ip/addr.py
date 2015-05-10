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

            if network.address:
                print("    inet/{proto} {addr} scope global {interface}".format(
                    proto=network.encapsulation.lower(),
                    addr=network.address,
                    interface=link.interface_name))

        def handle(self, context):
            networks_fetcher = context.client.network.list
            links_fetcher = context.client.link.list

            args = (context.args.datapath,)
            make_fetcher = lambda func: lambda *args: [func(*args)]

            if context.args.device:
                networks_fetcher = make_fetcher(context.client.network.get)
                links_fetcher = make_fetcher(context.client.link.get)
                args = (context.args.datapath, context.args.device)

            networks = networks_fetcher(*args)
            links = links_fetcher(*args)

            # sort devices by interface number
            predicate = lambda x: x.interface
            networks = sorted(networks, key=predicate)
            links = sorted(links, key=predicate)

            # render links and networks
            list(map(lambda args: self.render(*args), zip(links, networks)))

    class Module(core.BaseCommand):
        name = "module"
        aliases = ["mod"]
        help = "configure protocol modules"
        arguments = [
            (["module"],
             dict(metavar="NAME",
                  help="protocol module name",
                  nargs="?")),
        ]

        class Show(core.BaseCommand):
            name = "show"
            help = "look at protocol modules"

            def render(self, module):
                print("{name} <{state}> {desc}".format(
                    name=module.name,
                    state=module.state,
                    desc=module.description))

            def handle(self, context):
                modules_fetcher = context.client.netmod.list

                args = (context.args.datapath,)
                make_fetcher = lambda func: lambda *args: [func(*args)]

                if context.args.module:
                    modules_fetcher = make_fetcher(context.client.netmod.get)
                    args = (context.args.datapath, context.args.module)

                modules = modules_fetcher(*args)
                list(map(self.render, modules))


        class On(core.BaseCommand):
            name = "on"
            help = "turn on specified protocol module"

            def handle(self, context):
                context.client.netmod.enable(
                    datapath=context.args.datapath,
                    module=context.args.module)

        class Off(core.BaseCommand):
            name = "off"
            help = "turp off specified protocol module"

            def handle(self, context):
                context.client.netmod.disable(
                    datapath=context.args.datapath,
                    module=context.args.module)
