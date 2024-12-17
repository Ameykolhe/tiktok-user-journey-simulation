import os
import re

from setuptools import setup, find_packages


def get_version():
    init_path = os.path.join(os.path.dirname(__file__), "src/tiktok_simulator", "__init__.py")
    with open(init_path, "r") as f:
        for line in f:
            if line.startswith("__version__"):
                return re.search(r'"([^"]*)"', line).group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="tiktok-simulator",
    version=get_version(),  # Fetch version dynamically
    author="Amey Kolhe",
    author_email="kolheamey99@gmail.com",
    description="TikTok metadata scraper",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    python_requires=">=3.12"
)
