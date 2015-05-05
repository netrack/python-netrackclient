class BaseError(Exception):

    def __str__(self):
        err, *other = self.args
        if err:
            return "UNEXPERR: {0}".format(err.get("error"))

        return super(Exception, self).__str__()


class VersionError(BaseError):
    pass


class LinkError(BaseError):

    def __str__(self):
        err, *other = self.args
        if err:
            return "LINKERR: {0}".format(err.get("error"))

        return super(BaseError, self).__str__()


class NetworkError(BaseError):

    def __str__(self):
        err, *other = self.args
        if err:
            return "NETWERR: {0}".format(err.get("error"))

        return super(BaseError, self).__str__()


class RouteError(BaseError):

    def __str__(self):
        err, *other = self.args
        if err:
            return "ROUTEERR: {0}".format(err.get("error"))

        return super(BaseError, self).__str__()
