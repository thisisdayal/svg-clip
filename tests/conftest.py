"""Fixtures for pytest."""
import sys

import django
import pytest
from django.conf import settings as conf


# each test runs on cwd to its temp dir
@pytest.fixture(autouse=True)
def go_to_tmpdir(request):
    # Get the fixture dynamically by its name.
    tmpdir = request.getfixturevalue("tmpdir")
    # ensure local test created packages can be imported
    sys.path.insert(0, str(tmpdir))
    # Chdir only for the duration of the test.
    with tmpdir.as_cwd():
        yield


@pytest.fixture(scope="session")
def settings():
    conf.configure(
        DEBUG=True,
        INSTALLED_APPS=["svg_clip"],
        SECRET_KEY="dev",
        TEMPLATES=[
            {"BACKEND": "django.template.backends.django.DjangoTemplates"}
        ],
    )
    # To make sure settings is loaded before accessing settings variable
    django.setup()

    yield
