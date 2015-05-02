import argparse
import abc, six
import types
import importlib

from netrackclient.shell import mixin


@six.add_metaclass(abc.ABCMeta)
class Command(mixin.MetaMixin):
    __attributes__ = [
        "name",
        "aliases",
        "arguments",
        "help",
    ]

    def __init__(self):
        super(Command, self).__init__()

        self._command_chain = []

    def setup(self, subparsers):
        self.subcommands = {}

        self.subparser = subparsers.add_parser(
            name=self.__meta__.name,
            help=self.__meta__.help,
            aliases=(self.__meta__.aliases or []))

        for args, kwargs in self.__meta__.arguments or []:
            self.subparser.add_argument(*args, **kwargs)

        class_dict = self.__class__.__dict__
        filter_predicate = lambda o: isinstance(o, type)

        # search for sub-classes
        subcommands = filter(filter_predicate, class_dict.values())
        subcommands = list(subcommands)
        if not subcommands:
            self.subparser.set_defaults(func=self.handle)
            return

        subparsers = self.subparser.add_subparsers()

        for command_class in subcommands:
            command = command_class()
            command.setup(subparsers)
            self.subcommands[command_class.__name__] = command

    @abc.abstractmethod
    def handle(self, context):
        pass


class BaseCommand(Command):

    def handle(self, context):
        raise NotImplemented()


class Context(object):
    pass


class App(object):

    def __init__(self, prog, modules):
        super(App, self).__init__()

        self._modules = [m() for m in modules]
        self._parser = argparse.ArgumentParser(prog=prog)

    def setup(self):
        subparsers = self._parser.add_subparsers()

        for m in self._modules:
            m.setup(subparsers)

    def argument(self, args, kwargs):
        self._parser.add_argument(*args, **kwargs)

    def context(self, args):
        context = Context()
        context.args = args
        return context

    def start(self):
        args = self._parser.parse_args()

        # run handler
        args.func(self.context(args))
