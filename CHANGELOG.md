# Changelog


## (unreleased)

### Fix

* Updated kwargs_re to match all unicode characters. [Dayal Moirangthem]

### Other

* Chore: minor fixes. [Dayal Moirangthem]

* Chore: minor fixes. [Dayal Moirangthem]

* Chore: added extra dependencies. [Dayal Moirangthem]

* Docs: added instructions in README.md and minor modifications to other files. [Dayal Moirangthem]

* Refactor: refactoring code for distribution build. [Dayal Moirangthem]

  - added build method, Makefile.

  - included VERSION and pylintrc in MANIFEST.in.

  - added version detection in svg_clip package.

  - updated conftest.py.

  - refactored tests for better compliance to code formatters.

* Chore: tox.ini, requirements.txt, MANIFEST.in and Makefile are reconfigured. [Dayal Moirangthem]

* Test: removed vague tests. [Dayal Moirangthem]

  Removed tests for path returning multiple path (list or tuple) and removed malinformed argument test. Cannot find suitable test for malinformed arguments

* Refactor: code refactoring. [Dayal Moirangthem]

  Reduced the number of variables for better design.

* Chore: added tox and Makefile is changed to use tox. [Dayal Moirangthem]

* Refactor: code refactoring. [Dayal Moirangthem]

  Dictionary concatenation for new attributes has been shortned. Variable old attrs has been removed. 'key' and 'value' has replaced 'k', 'v' respectively.

* Chore: updated .coverage file to test `__repr__` method. [Dayal Moirangthem]

* Refactor: remove test for multiple icon paths. [Dayal Moirangthem]

  Since we cannot find any case for path to return a list or tuple, this test is vague so removed from the test

* Test: test for almost all of the possible cases covering the whole source code. [Dayal Moirangthem]

* Chore: added .coveragerc for code coverage configurations. [Dayal Moirangthem]

* Refactor: 'svg_clip.py' returning multiple paths for an icon. [Dayal Moirangthem]


## 0.1.0 (2023-02-11)

### Fix

* ClipNode must not have no child Nodes. [Dayal Moirangthem]

* ClipNode no longer accepts empty string value for svg_name. [Dayal Moirangthem]

  passing empty string value raises ValueError

### Other

* Release: version 0.1.0 🚀 [Dayal Moirangthem]

* Feat: added default icons. [Dayal Moirangthem]

  By default SVG clip uses heroiconsSVG's.

  set 'USE_CLIP_ICONS=True' in your 'DJANGO_SETTINGS_MODULE' to enable default icons.

* Wip: added compilation function for ClipNode. [Dayal Moirangthem]

  Implemented render method for rendering SVG markup with user provided attributes.

* Wip: added SVGParser for parsing SVG files and extract attributes. [Dayal Moirangthem]

* Wip: added custom exceptions. [Dayal Moirangthem]

* Test(passed)!:ClipNode repr test. [Dayal Moirangthem]

  - test with all valid arguments

  - test with valid svg_name, empty args and kwargs

  - test with empty string value for svg_name

  - test with no value for svg_name

  - test with no arguments

* Wip: created ClipNode for compilation function and added `__repr__` method. [Dayal Moirangthem]

* Chore: added templatetags module. [Dayal Moirangthem]

* Chore: deleted non-needed files `__main__.py`, `base.py`, `cli.py` [Dayal Moirangthem]

* Chore: updated different project files. [Dayal Moirangthem]

* ✅ Ready to clone and code. [thisisdayal]

* Initial commit. [Dayal Moirangthem]


