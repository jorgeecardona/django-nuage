import os
from setuptools import setup, find_packages

def get_packages():
    # setuptools can't do the job :(
    packages = []
    for root, dirnames, filenames in os.walk('nuage'):
        if '__init__.py' in filenames:
            packages.append(".".join(os.path.split(root)).strip("."))

    return packages

fd = open("README")
long_description = fd.read()
fd.close()

setup(
    name='nuage',
    version='0.2',
    description='django sdk for deployment in nuage infrastructure',
    author='Jorge Eduardo Cardona',
    author_email='jorge.cardona@cenuage.com',
    license="BSD",
    keywords="cloud django deployment",
    url="http://pypi.python.org/pypi/nuage/",
    long_description=long_description,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        ],
    )
