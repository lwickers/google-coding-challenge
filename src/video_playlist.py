"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, name):
        """The playlist class is initialised"""
        self._name = name
        self._videos = []
