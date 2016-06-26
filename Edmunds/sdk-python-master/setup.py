import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='edmunds',
    version='0.1.4',
    author='Michael Bock',
    author_email='api@edmunds.com',
    packages=['edmunds'],
    url='https://github.com/EdmundsAPI/sdk-python',
    license='LICENSE',
    description='This is an awesome Python 2 wrapper for the Edmunds.com API.',
    long_description=read('README.md'),
    install_requires=[
        "requests>=0.8.6",
    ],
)
