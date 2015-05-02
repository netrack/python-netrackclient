class Meta(object):

    def __init__(self, **kwargs):
        super(Meta, self).__init__()
        self._merge(**kwargs)

    def _merge(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class MetaMixin(object):

    def __init__(self, *args, **kwargs):
        super(MetaMixin, self).__init__()

        attributes = {}

        for attr in self.__attributes__:
            attributes[attr] = getattr(self, attr, None)

        self.__meta__ = Meta(**attributes)
