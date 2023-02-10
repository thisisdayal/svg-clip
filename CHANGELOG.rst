Changelog
=========


(unreleased)
------------

Fix
~~~
- ClipNode no longer accepts empty string value for svg_name. [Dayal
  Moirangthem]

  passing empty string value raises ValueError

Other
~~~~~
- Test(passed)!:ClipNode repr test. [Dayal Moirangthem]

  - test with all valid arguments

  - test with valid svg_name, empty args and kwargs

  - test with empty string value for svg_name

  - test with no value for svg_name

  - test with no arguments
- Wip: created ClipNode for compilation function and added `__repr__`
  method. [Dayal Moirangthem]
- Chore: added templatetags module. [Dayal Moirangthem]
- Chore: deleted non-needed files `__main__.py`, `base.py`, `cli.py`
  [Dayal Moirangthem]
- Chore: updated different project files. [Dayal Moirangthem]
- ✅ Ready to clone and code. [thisisdayal]
- Initial commit. [Dayal Moirangthem]


