#!/usr/bin/env python
from setuptools import setup


def main():
    setup(
        name='mypackage-name',
        version='1.0',
        description='My Package Description',
        url='https://my.package.url',
        author='Demo',
        author_email='contact@demo.com',
        packages=['mypackage.utils',
                  'mypackage.manager',
                  'mypackage.creator'],
        package_dir={'mypackage': 'mypackage'},
        zip_safe=False,
        install_requires=["requests >= 2.21.0",
                          "pytest",],
    )


if __name__ == '__main__':
    main()
