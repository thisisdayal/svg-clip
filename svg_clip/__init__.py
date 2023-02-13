"""Base module for Django SVG Clip."""
import io
import os


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("project_name", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


__version__ = read("svg_clip", "VERSION")
VERSION = __version__
