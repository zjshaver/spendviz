# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='spendviz',
    version='0.0.1',
    description='Financial transaction history visualizer',
    long_description=readme,
    author='Zachary Shaver',
    author_email='zjshaver@gmail.com',
    url='https://github.com/zjshaver/spendviz',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

