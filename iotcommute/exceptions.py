"""
Exceptions raised by the iot commute client
"""


class IotCommuteException(Exception):
    """Base exception class representing a IOTcommunicate client exception.
    Every specific IOTcommunicate client exception is a subclass of this
    and  exposes two instance variables	`.code` (HTTP error code)
    and `.message` (error text)."""

    def __init__(self, message, code=500):
        super(IotCommuteException, self).__init__(message)
        self.code = code
