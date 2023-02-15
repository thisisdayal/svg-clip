"""
Tests for SVG Clip

We make the test names as elaborate as possible to avoid
unnecessary comments.
"""
import pytest
from html.parser import HTMLParser

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings as SETTINGS
from django.template import Template, Context, TemplateSyntaxError

from svg_clip.templatetags.svg_clip import ClipNode
from svg_clip.exceptions import SVGIconNotFound


class TestClipNode:
    """Test for ClipNode."""

    def test_clip_node(self) -> None:
        # test typical ClipNode with all arguments
        assert (
            repr(
                ClipNode(
                    "academic-cap",
                    args=["required", "hidden"],
                    kwargs={"class": "h-6 w-6 text-green-500"},
                )
            )
            == "<ClipNode svg_name='academic-cap.svg' args=['required', "
            "'hidden'] kwargs={'class': 'h-6 w-6 text-green-500'}>"
        )

    def test_ClipNode_with_no_args_and_kwargs(self):
        assert (
            repr(ClipNode("academic-cap", args=[], kwargs={}))
            == "<ClipNode svg_name='academic-cap.svg' args=[] kwargs={}>"
        )

    def test_ClipNode_with_empty_string(self):
        with pytest.raises(ValueError):
            repr(ClipNode("", args=[], kwargs={}))

    def test_ClipNode_with_args_and_kwargs_only(self):
        with pytest.raises(TypeError):
            repr(ClipNode(args=[], kwargs={}))

    def test_ClipNode_with_no_arguments(self):
        with pytest.raises(TypeError):
            repr(ClipNode())


class TestClipTag:
    """Test for template tag."""

    context = Context()

    def test_render_tag_with_args_and_kwargs(self, settings):
        SETTINGS.USE_CLIP_ICONS = True
        template = Template(
            '{% load svg_clip %} {% clip "arrow-down" '
            'class="h-6 w-6" "hidden" %}'
        )
        assert HTMLParser().feed(
            template.render(self.context)
        ) == HTMLParser().feed(
            '<svg class="h-6 w-6" hidden xmlns="http://www.w3.org/2000/svg" '
            'fill="none" viewBox="0 0 24 24" stroke-width="1.5" '
            'stroke="currentColor" aria-hidden="true"> <path '
            'stroke-linecap="round" stroke-linejoin="round" '
            'd="M19.5 13.5L12 21m0 0l-7.5-7.5M12 21V3"/></svg>'
        )

    def test_render_tag_with_kwargs(self, settings):
        template = Template(
            '{% load svg_clip %} {% clip "arrow-down" class="h-6 w-6" %}'
        )
        assert HTMLParser().feed(
            template.render(self.context)
        ) == HTMLParser().feed(
            '<svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" '
            'fill="none" viewBox="0 0 24 24" stroke-width="1.5" '
            'stroke="currentColor" aria-hidden="true"> <path '
            'stroke-linecap="round" stroke-linejoin="round" '
            'd="M19.5 13.5L12 21m0 0l-7.5-7.5M12 21V3"/></svg>'
        )

    def test_render_tag_with_kwargs_already_present(self, settings):
        template = Template(
            '{% load svg_clip %} {% clip "arrow-down" '
            'class="h-6 w-6" aria-hidden="true" %}'
        )
        assert HTMLParser().feed(
            template.render(self.context)
        ) == HTMLParser().feed(
            '<svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" '
            'fill="none" viewBox="0 0 24 24" stroke-width="1.5" '
            'stroke="currentColor" aria-hidden="true"> <path '
            'stroke-linecap="round" stroke-linejoin="round" '
            'd="M19.5 13.5L12 21m0 0l-7.5-7.5M12 21V3"/></svg>'
        )

    def test_render_tag_with_args(self, settings):
        template = Template(
            '{% load svg_clip %} {% clip "arrow-down" "hidden" %}'
        )
        assert HTMLParser().feed(
            template.render(self.context)
        ) == HTMLParser().feed(
            '<svg hidden xmlns="http://www.w3.org/2000/svg" '
            'fill="none" viewBox="0 0 24 24" stroke-width="1.5" '
            'stroke="currentColor" aria-hidden="true"> <path '
            'stroke-linecap="round" stroke-linejoin="round" '
            'd="M19.5 13.5L12 21m0 0l-7.5-7.5M12 21V3"/></svg>'
        )

    def test_render_tag_with_no_args_and_kwargs(self, settings):
        template = Template('{% load svg_clip %} {% clip "arrow-down" %}')
        assert HTMLParser().feed(
            template.render(self.context)
        ) == HTMLParser().feed(
            '<svg xmlns="http://www.w3.org/2000/svg" fill="none" '
            'viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" '
            'aria-hidden="true"> <path stroke-linecap="round" '
            'stroke-linejoin="round" d="M19.5 13.5L12 '
            '21m0 0l-7.5-7.5M12 21V3"/></svg>'
        )

    def test_render_tag_with_no_arguments(self, settings):
        with pytest.raises(TemplateSyntaxError):
            assert Template("{% load svg_clip %} {% clip %}")

    def test_svg_icons_dir_typecheck(self, settings):
        with pytest.raises(ImproperlyConfigured):
            SETTINGS.SVG_ICONS_DIRS = ()
            template = Template('{% load svg_clip %} {% clip "arrow-down" %}')
            template.render(self.context)

    def test_svg_icons_dir_empty(self, settings):
        with pytest.raises(ImproperlyConfigured):
            SETTINGS.SVG_ICONS_DIRS = []
            SETTINGS.USE_CLIP_ICONS = False
            template = Template('{% load svg_clip %} {% clip "arrow-down" %}')
            template.render(self.context)

    def test_svg_icons_dir_not_set(self, settings):
        SETTINGS.USE_CLIP_ICONS = False
        with pytest.raises(ImproperlyConfigured):
            template = Template('{% load svg_clip %} {% clip "flying-jet" %}')
            template.render(self.context)

    def test_svg_icon_not_found(self, settings):
        SETTINGS.USE_CLIP_ICONS = True
        with pytest.raises(SVGIconNotFound):
            template = Template('{% load svg_clip %} {% clip "flying-jet" %}')
            template.render(self.context)

    def test_svg_icon_not_found_production(self, settings):
        # Should not raise error, instead log warning in production
        SETTINGS.DEBUG = False
        SETTINGS.USE_CLIP_ICONS = True
        template = Template('{% load svg_clip %} {% clip "flying-jet" %}')
        template.render(self.context)

    # FIXME: Test to return multiple paths
    # def test_svg_icons_more_than_one(self, settings):
    #     # Return first matching icon if found a list
    #     SETTINGS.SVG_ICONS_DIRS = ["icons", "icons copy"]
    #     SETTINGS.USE_CLIP_ICONS = True
    #     template = Template('{% load svg_clip %} {% clip "arrow-down" %}')
    #     template.render(self.context)

    # TODO: Cannot find a suitable test for malinformed arguments
    # def test_svg_clip_malinformed_arguments(self, settings):
    #     SETTINGS.USE_CLIP_ICONS = True
    #     # Malinformed arguments
    #     with pytest.raises(TemplateSyntaxError):
    #         template = Template(
    #             '{% load svg_clip %} {% clip "arrow-down" class="<>" %}'
    #         )
    #         template.render(self.context)
