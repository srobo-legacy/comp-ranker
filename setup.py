from setuptools import find_packages, setup


with open('README.md') as f:
    description = f.read()


setup(name='sr.ranker',
      version='1.0.0',
      packages=find_packages(),
      namespace_packages=['sr', 'sr.comp'],
      description=description,
      author='Student Robotics Competition Software SIG',
      author_email='srobo-devel@googlegroups.com',
      install_requires=['nose >=1.3, <2'],
      zip_safe=True)
