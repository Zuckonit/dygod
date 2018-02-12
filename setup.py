#coding: utf-8

from setuptools import setup, find_packages

setup(
    name='dygod',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Click',
        'requests',
        'fake_useragent'
    ],
    entry_points='''
        [console_scripts]
        dygod=dygod.cmd:cli
    ''',
)
