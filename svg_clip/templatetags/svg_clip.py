"""Templatetags used in svg-clip"""
import re
import logging

from pathlib import Path

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template import Library, Node, TemplateSyntaxError
from django.template.context import Context
from django.utils.safestring import mark_safe

import svg_clip

from svg_clip.exceptions import SVGIconNotFound
from svg_clip.parsers import SVGParser


logger = logging.getLogger(__name__)
register = Library()


# Base path from which all the relative files must be built
ANCHOR_BASE = Path(svg_clip.__file__).resolve().parent

# Heroicons icon folders for default icons
HEROICONS_DIRS = [
    ANCHOR_BASE / "heroicons" / "solid",
    ANCHOR_BASE / "heroicons" / "outline",
]

# Patterns
svgtag = re.compile("^<svg([^<]*)>")
kwarg_re = re.compile(r"(?:([\w-]+)=)?(.+)", re.UNICODE)
# kwarg_re = _lazy_re_compile(r"(?:([\w-]+)=)?([\"|\'][\w\s-]+[\'|\"])")


class ClipNode(Node):
    """Implement the functions of clip tag."""

    child_nodelists = ()

    def __init__(self, svg_name, args: list, kwargs: dict) -> None:
        self.svg_name = svg_name
        self.args = args
        self.kwargs = kwargs

        if str(self.svg_name).strip() == "":
            raise ValueError('"svg_name" cannot be empty string!')

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__qualname__} svg_name='{self.svg_name}.svg' "
            f"args={repr(self.args)} kwargs={repr(self.kwargs)}>"
        )

    def render(self, context: Context) -> str:
        svg_name: str = f"{self.svg_name.resolve(context)}.svg"
        args: list = [arg.resolve(context) for arg in self.args]
        kwargs: dict = {k: v.resolve(context) for k, v in self.kwargs.items()}

        svg_icons_dirs = getattr(settings, "SVG_ICONS_DIRS", [])

        # `SVG_ICONS_DIRS` must be a list.
        if not isinstance(svg_icons_dirs, list):
            raise ImproperlyConfigured(
                f"'SVG_ICONS_DIRS' must be list but given "
                f"{type(svg_icons_dirs).__name__}! "
            )

        # Get attribute `USE_CLIP_ICONS` from settings.
        # If not set, default value is False.
        # If True, use default icons(HEROICONS_DIRS).
        if getattr(settings, "USE_CLIP_ICONS", False):
            svg_icons_dirs += HEROICONS_DIRS

        # Empty `SVG_ICONS_DIRS` should raise error.
        if len(svg_icons_dirs) == 0:
            raise ImproperlyConfigured(
                "No 'SVG_ICONS_DIRS' Found! "
                "Set 'USE_CLIP_ICONS' to True to use default icons."
            )

        path = None
        # set path to absolute icon path if found.
        for directory in svg_icons_dirs:
            svg_path = Path(directory) / svg_name
            if svg_path.is_file():
                path = svg_path

        if not path:
            message = f"SVG {svg_name} not found!"
            if settings.DEBUG:
                raise SVGIconNotFound(message)
            logger.warning(message)
            return ""

        # I don't find no case for returning multiple paths,
        # so ommited this block.
        # If multiple paths found return the first one.
        # if isinstance(path, (list, tuple)):
        #     path = path[0]

        with open(path, encoding="utf-8") as file:
            raw_svg = file.read()

        # Get the attributes from the svg and concatenate
        # with the user provided attrs from the tag
        new_attrs: dict = {**kwargs, **SVGParser().extract(raw_svg)}

        # Join the dictionary to form 'key="value"' pair string
        kw_attrs = " ".join(f'{k}="{v}"' for k, v in new_attrs.items())
        attrs = " ".join(args)

        # Return the safestring with new svg starttag
        return mark_safe(
            re.sub(svgtag, r"<svg " + kw_attrs + attrs + ">", raw_svg)
        )


@register.tag
def clip(parser, token):
    """
    Render the svg icon along with user provided attributes
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError(
            f"'{bits[0]}' takes at least one argument, a svg icon name."
        )

    svgname = parser.compile_filter(bits[1])
    args = []
    kwargs = {}
    bits = bits[2:]

    for bit in bits:
        match = kwarg_re.match(bit)
        if not match:
            raise TemplateSyntaxError("Malformed arguments to clip tag")
        name, value = match.groups()
        if name:
            kwargs[name] = parser.compile_filter(value)
        else:
            args.append(parser.compile_filter(value))

    return ClipNode(svgname, args, kwargs)
