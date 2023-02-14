"""Parsers used for parsing SVG."""
from html.parser import HTMLParser
from typing import Union


class SVGParser(HTMLParser):
    """Find tags and other markup and call handler functions.

    Usage:
        p = SVGParser()
        p.feed(data)
        ...
        p.close()

    Start tags are handled by calling self.handle_starttag().
    self.handle_starttag() find svg starting tags and add the
    attributes to self.attrs.
    non-keyword attributes are added with None as value."""

    def __init__(self, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        # add attributes dict
        self.attrs: dict[str, Union[str, None]] = {}

    def handle_starttag(self, tag, attrs) -> None:
        "if tag is svg then populate self.attrs"
        if tag == "svg":
            self.attrs = dict(attrs)
        return super().handle_starttag(tag, attrs)

    def extract(self, data: str) -> dict[str, Union[str, None]]:
        "Return the attributes of svg tag."
        self.feed(data)
        return self.attrs
