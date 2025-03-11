import re

from setuptools import find_packages, setup

setup(
     version=re.search(
        r'^version\s*=\s*"(.*?)"', open("pyproject.toml").read(), re.M
    ).group(1),
    packages=find_packages(),
)
