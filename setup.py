"""
495 python package configuration.

"""

from setuptools import setup

setup(
    name='ICUDiary',
    version='0.1.0',
    packages=['ICUDiary'],
    include_package_data=True,
    install_requires=[
        'arrow',
        'bs4',
        'Flask',
        'html5validator',
        'pycodestyle',
        'pydocstyle',
        'pylint',
        'pytest',
        'requests',
        'selenium',
    ],
    python_requires='>=3.6',
)
