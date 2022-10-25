from setuptools import setup
import sys, re, pathlib
from os import system

# 'setup.py publish' shortcut.
if sys.argv[-1] == "publish":
    system("rm -rf dist && python setup.py sdist bdist_wheel")
    system("twine upload dist/*")
    sys.exit()

here = pathlib.Path(__file__).parent
long_description = (here / "README.md").read_text("utf-8")
about = (here / "src" / "ynam" / "_version.py").read_text("utf-8")


def read_from_file(key):
    return re.search(f"{key} = ['\"]([^'\"]+)['\"]", about).group(1)


setup(name=read_from_file("__title__"),
      version=read_from_file("__version__"),
      package_dir={"": "src"},
      include_package_data=True,
      description=read_from_file("__description__"),
      url=read_from_file("__url__"),
      license=read_from_file("__license__"),
      author=read_from_file("__author__"),
      author_email=read_from_file("__author_email__"),
      long_description_content_type="text/markdown",
      packages=["ynam"],
      install_requires=[
          "mintapi",
      ],
      entry_points={"console_scripts": ["ynam = ynam.main:main"]})
