class BaseError(Exception):
    pass


class VersionError(BaseError):
    pass


class LinkError(BaseError):
    pass


class LinkAddressFormatError(LinkError):
    pass


class NetworkError(BaseError):
    pass


class NetworkAddressFormatError(NetworkError):
    pass
