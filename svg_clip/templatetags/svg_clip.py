"""Templatetags used in svg-clip"""
from django.template import Node


class ClipNode(Node):
    def __init__(self, svg_name, args, kwargs) -> None:
        self.svg_name = svg_name
        self.args = args
        self.kwargs = kwargs

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__qualname__} svg_name="{self.svg_name}.svg" '
            f"args={repr(self.args)} kwargs={repr(self.kwargs)}>"
        )
