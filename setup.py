import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 10, 0):
    raise RuntimeError("ynam requires Python 3.10.0+")

setup(
    name="YNAM (You Need a Mint)",
    version='0.1.0',
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    description="Mint-to-YNAB translation layer",
    url="https://githuib.com/snowskeleton/ynam",
    license="Apache 2.0",
    author="snowskeleton",
    author_email="snow@snowskeleton.net",
    keywords="ynab, mint",
    long_description_content_type="text/markdown"
)
