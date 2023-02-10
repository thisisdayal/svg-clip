import pytest

from svg_clip.templatetags.svg_clip import ClipNode


def test_clip_node() -> None:
    # test typical ClipNode with all arguments
    assert (
        repr(
            ClipNode(
                "academic-cap",
                args=["required", "hidden"],
                kwargs={"class": "h-6 w-6 text-green-500"},
            )
        )
        == "<ClipNode svg_name='academic-cap.svg' args=['required', 'hidden'] "
        "kwargs={'class': 'h-6 w-6 text-green-500'}>"
    )

    # test ClipNode with no args and kwargs
    assert (
        repr(ClipNode("academic-cap", args=[], kwargs={}))
        == "<ClipNode svg_name='academic-cap.svg' args=[] kwargs={}>"
    )

    # test ClipNode with empty_string
    with pytest.raises(ValueError):
        repr(ClipNode("", args=[], kwargs={}))

    # test ClipNode with args and kwargs only
    with pytest.raises(TypeError):
        repr(ClipNode(args=[], kwargs={}))

    # test ClipNode with no arguments
    with pytest.raises(TypeError):
        repr(ClipNode())
