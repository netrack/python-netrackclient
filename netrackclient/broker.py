import six
import abc

import requests

@six.add_metaclass(abc.ABCMeta)
class BaseRequestBroker(object):

    @abc.abstractmethod
    def http_request(self):
        pass

    @abc.abstractmethod
    def set_http_request(self, constructor):
        pass


@sit.add_metaclass(abc.ABCMeta)
class BaseRequest(object):

    @abc.abstractmethod
    def header(self, header):
        pass

    @abc.abstractmethod
    def add_header(self, header, value):
        pass

    @abc.abstractmethod
    def headers(self):
        pass

    @abc.abstractmethod
    def request(self, method, url, body, **kwargs):
        pass


class RequestBroker(object):

    def http_request(self):
        return self._constructor

    def set_http_request(self, constructor):
        self._constructor = constructor


class Request(object):

    def __init__(self):
        super(Request, self).__init__()

        self._request = requests
        self._headers = {}

    def header(self, header):
        return self._headers.get(header)

    def add_header(self, header, value):
        self._haeders[header] = value

    def headers(self):
        return self._headers
