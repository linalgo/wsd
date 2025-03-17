"""WSD package setup script."""
import re

from setuptools import find_packages, setup

with open("pyproject.toml", encoding="utf-8")  as file:
    setup(
        version=re.search(
            r'^version\s*=\s*"(.*?)"',  file.read(), re.M
        ).group(1),
        packages=find_packages(),
    )
