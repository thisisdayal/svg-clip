<h1 align="center">
  <br>
  <br>
  Django-svg-clip
  <br>
  <br>
</h1>

<div align="center">
  <a href="https://codecov.io/gh/thisisdayal/svg-clip" >
    <img src="https://codecov.io/gh/thisisdayal/svg-clip/branch/main/graph/badge.svg?token=VPY6PPFO1I"/>
  </a>
  <a href="https://github.com/thisisdayal/svg-clip/actions/workflows/main.yml">
    <img src="https://github.com/thisisdayal/svg-clip/actions/workflows/main.yml/badge.svg"/>
  </a>
  <a href="https://github.com/thisisdayal/svg-clip/actions/workflows/release.yml">
    <img src="https://github.com/thisisdayal/svg-clip/actions/workflows/release.yml/badge.svg"/>
  </a>
</div>

<p align="center">Django-svg-clip is a django template tags plugin for manipulating and rendering of svg and its attributes.</p>

## Features

- Adding static and dynamic attributes to svg icons.
- You don't have to paste the whole svg tag to add atrributes such as classes, inline-styles, WAI-arias.
- Makes the template look cleaner and shorter.
- Increases the readability.

## Installation

Install django-svg-clip from PyPI by running:

```bash
# shell
pip install django-svg-clip
```

## Setup

1. After installing add `svg_clip` to `INSTALLED_APPS` in the `DJANGO_SETTINGS_MODULE`(e.g. settings.py).

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'svg_clip',
]
```

2. Add SVG icons path to `SVG_ICONS_DIRS`:

```python
# settings.py
SVG_ICONS_DIRS = [
    # path/to/icons
    # E.g:
    BASE_DIR / "static" / "heroicons" / "outline",
    BASE_DIR / "static/heroicons/solid",
    BASE_DIR / "static" / "icons",
    BASE_DIR / "static/icons",
]
```

3. Or you can use default icons by setting `USE_CLIP_ICONS` to `True`.

```python
# settings.py
USE_CLIP_ICONS = True
```

## Usage

After adding the path of icons, use this tag `{% clip 'icon-name' keyword_attrs="key word attrs" "non-keyword" "attrs" %}` to add the icons to the django template.

**NOTE**: Don't put `.svg` extension to the icons, it is automatically added during compilation.

```xml
<!-- template.html -->
<!DOCTYPE html>
{% load svg_clip %}
<html>
  <head>
    <!-- ...  -->
  </head>
  <body>
    <!-- ...  -->
    {% clip 'academic-cap' %}
    {% clip 'academic-cap' class="h-6 w-6" %}
    {% clip 'academic-cap-solid' class="h-6 w-6" styles="display: block" %}
    {% clip 'academic-cap' class="h-6 w-6" styles="display: block" "hidden" %}
  </body>
</html>
```

_**Remarks**: The defult icon set is heroicons-v2.0.13. To use the outline version, just use the icon name and for solid version, add `'-solid'` suffix to the icon name. For example, to use `'academic-cap.svg'` outline version, just use `'academic-cap'` and for solid version use `'academic-cap-solid'`._

## Development

- Issue Tracker: [Github Issues](https://github.com/thisisdayal/svg-clip/issues)
- Source Code: [Github repo](https://github.com/thisisdayal/svg-clip/)

_**NOTE**: For contributing read the [CONTRIBUTING.md](CONTRIBUTING.md) file._

## Support

If you are having issues, please let us know by opening an issue in our github repo. We warmly welcome you for any suggestion.

## License

The project is licensed under the MIT license giving the community maximum priviledge to use. For more read [LICENSE.md](LICENSE.md) file.

## Author

Name: **Dayal Moirangthem**\
Twitter: [@thisisdayal](https://twitter.com/thisisdayal)

## Acknowledgement and credits

[**Heroicons**](https://heroicons.com/): By default, we use icon set provided by heroicons with a minimal tweaks in icon names. For example, let us say `academic-cap.svg`. For outline version, there is no modification but for solid, you should use `academic-cap-solid.svg`.This is done to avoid name conflicts with outline and solid versions.

We'd like to show our regards to tailwindlabs team for availing those icons to community with an open source license.

[**Python project template**](https://github.com/rochacbruno/python-project-template/): We use `rochacbruno`'s python project template with little modification. It saves us a lot of time and headache during initial setup.
