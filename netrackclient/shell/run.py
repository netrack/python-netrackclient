from netrackclient import netrack
from netrackclient.netrack.v1 import client
from netrackclient.shell import core
from netrackclient.shell.commands import ip


class App(core.App):

    def context(self, args):
        context = core.Context()

        # save parsed arguments
        context.args = args

        # create netrack client
        context.client = client.Client(
            service_url=args.service_url)

        return context


def main():
    try:
        # create an application
        app = App(prog="netrack", modules=[ip.IP])

        # setup the application
        app.setup()

        app.argument(["-s", "--service-url"],
            dict(help="service endpoint",
                 default="http://127.0.0.1:8080"))

        app.argument(["-d", "--datapath"],
            dict(help="OpenFlow switch identifier"))

        app.argument(["-v", "--version"],
            dict(help="print version and exit",
                 action="version",
                 version="%(prog)s {0}".format(netrack.__version__)))

        # run the application
        app.start()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
