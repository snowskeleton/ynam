from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent

long_description = (pathlib.Path(__file__).parent,
                    "README.md").read_text("utf-8")

setup(author='snowskeleton',
      author_email='isaac@snowskeleton.net',
      description='Mint to YNAB translator',
      include_package_data=True,
      keywords="ynab, mint",
      license='Apache 2.0',
      long_description_content_type="text/markdown",
      long_descriptin=long_description,
      name='ynam',
      package_dir={"": "src"},
      packages=find_packages("src"),
      url='https://github.com/snowskeleton/ynam',
      version='v0.1.1',
      install_requires=[
          'mintapi',
      ],
      entry_points={"console_scripts": ["ynam = ynam.main:run"]})
