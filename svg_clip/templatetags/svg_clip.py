"""Templatetags used in svg-clip"""
import re
import logging
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template import Node
from django.template.context import Context
from django.utils.regex_helper import _lazy_re_compile
from django.utils.safestring import mark_safe

import svg_clip
from svg_clip.exceptions import SVGIconNotFound
from svg_clip.parsers import SVGParser


logger = logging.getLogger(__name__)


# Base path from which all the relative files must be built
ANCHOR_BASE = Path(svg_clip.__file__).resolve().parent

# Heroicons icon folders for default icons
HEROICONS_DIRS = [
    ANCHOR_BASE / "heroicons" / "solid",
    ANCHOR_BASE / "heroicons" / "outline",
]

# Patterns
svgtag = re.compile("^<svg([^<]*)>")
kwarg_re = _lazy_re_compile(r"(?:([\w-]+)=)?(.+)")


class ClipNode(Node):
    child_nodelists = ()

    def __init__(self, svg_name: str, args: list, kwargs: dict) -> None:
        self.svg_name = svg_name
        self.args = args
        self.kwargs = kwargs

        if self.svg_name.strip() == "":
            raise ValueError('"svg_name" cannot be empty string!')

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__qualname__} svg_name='{self.svg_name}.svg' "
            f"args={repr(self.args)} kwargs={repr(self.kwargs)}>"
        )

    @mark_safe
    def render(self, context: Context) -> str:
        svg_name: str = f"{self.svg_name.resolve(context)}.svg"
        args: list = [arg.resolve(context) for arg in self.args]
        kwargs: dict = {k: v.resolve(context) for k, v in self.kwargs.items()}

        svg_icons_dirs = getattr(settings, "SVG_ICONS_DIRS", [])

        # `SVG_ICONS_DIRS` must be a list
        if not isinstance(svg_icons_dirs, list):
            raise ImproperlyConfigured(
                f"'SVG_ICONS_DIRS' must be list but given \
                    {type(svg_icons_dirs).__name__}"
            )

        # Use default icons if True
        use_clip_icons = getattr(settings, "USE_CLIP_ICONS", False)
        if use_clip_icons:
            svg_icons_dirs += HEROICONS_DIRS

        path = None
        # set path to absolute icon path if found
        for directory in svg_icons_dirs:
            svg_path = Path(directory) / svg_name
            if svg_path.is_file():
                path = svg_path

        if not path:
            message = f"SVG {svg_name} not found!"
            if settings.DEBUG:
                raise SVGIconNotFound(message)
            else:
                logger.warning(message)
                return ""

        # If multiple paths found return the first one
        if isinstance(path, (list, tuple)):
            path = path[0]

        with open(path, encoding="utf-8") as f:
            raw_svg = f.read()
            # Get the attributes from the svg
            old_attrs = SVGParser().feed(raw_svg)

        new_attrs: dict = kwargs

        svghead = r"<svg "

        for k, v in new_attrs.items():
            if k not in old_attrs and k is not None:
                svghead += f' {k}="{v}"'

        for k, v in old_attrs.items():
            svghead += f' {k}="{v}"'

        if len(args) != 0:
            for arg in args:
                svghead += f" {arg}"

        new_svgtag = svghead + ">"

        svg = re.sub(svgtag, new_svgtag, raw_svg)

        return svg
