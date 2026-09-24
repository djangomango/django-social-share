#!/usr/bin/env python
import sys
from pathlib import Path
from typing import Any

import django
import django.test.utils
from django.conf import settings

base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir.parent))

settings.configure(
    SITE_ID=1,
    DATABASES={
        "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"},
    },
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.sessions",
        "django.contrib.contenttypes",
        "django_social_share",
        "django_social_share.tests",
    ],
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [
                base_dir / "templates",
            ],
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.request",
                ],
            },
        },
    ],
)


def runtests(*test_args: Any) -> None:
    """Execute Django test runner for test suite."""
    django.setup()
    runner_class = django.test.utils.get_runner(settings)
    test_runner = runner_class(verbosity=1, interactive=True)
    failures = test_runner.run_tests(["django_social_share"])
    sys.exit(failures)


if __name__ == "__main__":
    runtests()
