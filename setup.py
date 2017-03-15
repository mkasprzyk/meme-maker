#!/usr/bin/env python
from setuptools import setup, find_packages
from setuptools.command.install import install
import unittest
import pip

import os
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


class SetupTypes:
    SERVERLESS = 'serverless'
    BASE = 'base'

    @staticmethod
    def requirements(setup_type):
        requirements_path_pattern = 'requirements/{setup_type}.txt'
        return requirements_path_pattern.format(
            setup_type=setup_type
        )


class CustomInstall(install):

    user_options = [
        ('setup-type=', None, 'Specify setup type ({})'.format(
            ','.join([SetupTypes.SERVERLESS, SetupTypes.BASE])
        )),
   ] + install.user_options

    def initialize_options(self):
        super(CustomInstall, self).initialize_options()
        self.setup_type = SetupTypes.BASE

    def finalize_options(self):
        super(CustomInstall, self).finalize_options()
        assert self.setup_type in (None, SetupTypes.BASE, SetupTypes.SERVERLESS), 'Invalid setup type!'

    def prepare_requirements(self):
        requirements = os.path.join(os.getcwd(), SetupTypes.requirements(self.setup_type))
        assert os.path.exists(requirements), 'Invalid requirements path!'
        return requirements

    def install_from_dist(self):
        pip_params = ['install', '-r', self.prepare_requirements()]
        pip.main(pip_params)

    def run(self):
        self.install_from_dist()
        install.run(self)


def tests():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('meme_maker.tests', pattern='test_*.py')
    return test_suite

install_requires = ['setuptools']

setup(name="meme-maker",
    license = "MIT",
    version=0.1,
    description="CLI, API and Slack bot to generate memes. Make memes not war.",
    maintainer="Jacek Szubert",
    author="Jacek Szubert",
    author_email="",
    url="https://github.com/jacekszubert/meme-maker",
    keywords="meme, memes, slack, bot, api, cli, generator",
    classifiers=["Development Status :: 0.1 - Beta",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: BSD License",
                 "Programming Language :: Python",
                 "Topic :: Software Development :: Libraries :: Python Modules",
                 ],
    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'meme-maker = meme_maker.__main__:cli',
        ]
    },
    cmdclass={
        'install': CustomInstall
    },
    test_suite='setup.tests',
)
