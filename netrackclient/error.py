class BaseError(Exception):
    pass


class LinkError(BaseError):
    pass


class LinkAddressFormatError(LinkError):
    pass


class NetworkError(BaseError):
    pass


class NetworkAddressFormatError(NetworkError):
    pass
