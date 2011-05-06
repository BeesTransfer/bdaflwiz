"""
Provides the default configuration for :mod:`bdaflwiz` module.
"""

import urllib

class Configuration(object):
    """
    Provides a configuration class for the entire :mod:`bdaflwiz`
    module.
    """

    def __init__(self,
                 protocol="http",
                 host="trackntrace.aflwiz.com",
                 port=80,
                 uri="/aflwiztrack",
                 search_key="shpntrefnum"):
        """
        Constructs the :class:`Configuration` class instance.
        """
        self.protocol = protocol
        self.host = host
        self.port = port
        self.uri = uri
        self.search_key = search_key

    @property
    def _url_template(self):
        """
        Returns the URI for the AFL endpoint.
        """
        return "%s://%s:%d%s" % (
            self.protocol,
            self.host,
            self.port,
            self.uri)

    def get_url(self, search_value, search_key=None):
        """
        Returns the URL for the shipment track resource.
        """
        if not search_key:
            search_key = self.search_key

        # Construct search parameters:
        params = urllib.urlencode({search_key: search_value})

        # Construct and return the URL:
        return "%s?%s" % (self._url_template, params)

