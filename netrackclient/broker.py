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


@six.add_metaclass(abc.ABCMeta)
class BaseRequest(object):

    @abc.abstractmethod
    def add_header(self, header, value):
        pass

    @abc.abstractmethod
    def get(self, url, body, **kwargs):
        pass

    @abc.abstractmethod
    def put(self, url, body, **kwargs):
        pass

    @abc.abstractmethod
    def delete(self, url, body, **kwargs):
        pass


@six.add_metaclass(abc.ABCMeta)
class BaseResponse(object):

    @abc.abstractmethod
    def header(self, header):
        pass

    @abc.abstractmethod
    def headers(self):
        pass

    @abc.abstractmethod
    def body(self):
        pass

    @abc.abstractmethod
    def status(self):
        pass


class RequestBroker(object):

    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def http_request(self):
        return self._constructor()

    def set_http_request(self, constructor):
        self._constructor = constructor


class Response(BaseResponse):

    def __init__(self, response):
        super(Response, self).__init__()

        self._response = response

    def header(self, header):
        return self._response.headers[header]

    def headers(self):
        return self._response.headers

    def body(self):
        return self._response.json()

    def status(self):
        return self._response.status_code


class Request(object):

    def __init__(self):
        super(Request, self).__init__()

        # use requests library
        self._request = requests
        self._headers = {}

    def add_header(self, header, value):
        self._headers[header] = value

    def get(self, url, **kwargs):
        response = self._request.get(
            url,
            headers=self._headers,
            **kwargs)

        return Response(response)

    def put(self, url, body, **kwargs):
        response = self._request.put(
            url,
            headers=self._headers,
            data=body,
            **kwargs)

        return Response(response)

    def delete(self, url, body, **kwargs):
        response = self._request.delete(
            url,
            headers=self._headers,
            data=body,
            **kwargs)

        return Response(response)


__broker = RequestBroker()
__broker.set_http_request(Request)
