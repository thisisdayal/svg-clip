"""Parsers used for parsing SVG."""
from html.parser import HTMLParser


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

    def __init__(self, *, convert_charrefs: bool = ...) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.attrs = {}

    def feed(self, data: str) -> dict[str, str | None]:
        super().feed(data)
        return self.attrs

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        if tag == "svg":
            self.attrs = dict(attrs)
        return super().handle_starttag(tag, attrs)
