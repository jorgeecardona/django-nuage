import os
from distutils.core import setup


def get_packages():
    # setuptools can't do the job :(
    packages = []
    for root, dirnames, filenames in os.walk('nuage'):
        if '__init__.py' in filenames:
            packages.append(".".join(os.path.split(root)).strip("."))

    return packages


setup(
    name='nuage',
    version='1.2',
    description='django sdk for deployment in nuage infrastructure',
    author='Jorge Eduardo Cardona',
    author_email='jorgeecardona@gmail.com',
    packages=get_packages(),
    )
