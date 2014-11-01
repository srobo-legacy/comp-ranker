from setuptools import setup

with open('README.md') as f:
    description = f.read()

setup(name = "sr-ranker",
      version = "1.0",
      packages = ['sr.comp.ranker'],
      description = description,
      author = "Peter Law",
      author_email = "PeterJCLaw@gmail.com",
      install_requires = ['nose >=1.3, <2'],
      zip_safe = True
      )

