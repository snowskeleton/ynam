from setuptools import setup, find_packages
import pathlib, re

here = pathlib.Path(__file__).parent

long_description = (here / "README.md").read_text("utf-8")

about = (here / "src" / "audible_cli" / "_version.py").read_text("utf-8")


def read_from_file(key):
    return re.search(f"{key} = ['\"]([^'\"]+)['\"]", about).group(1)

setup(
    author=read_from_file("__author__"),
    author_email=read_from_file("__author_email__"),
    description=read_from_file("__description__"),
    include_package_data=True,
    keywords="ynab, mint",
    license=read_from_file("__license__"),
    long_description_content_type="text/markdown",
    name=read_from_file("__title__"),
    package_dir={"": "src"},
    packages=find_packages("src"),
    url=read_from_file("__url__"),
    version=read_from_file("__version__"),
    install_requires=[
        'mintapi',
    ],
)
