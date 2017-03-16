#!/usr/bin/env python
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.sdist import sdist
from setuptools.command.egg_info import egg_info

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


class CustomCommand(object):

    user_options = [
        ('setup-type=', None, 'Specify setup type ({})'.format(
            ','.join([SetupTypes.SERVERLESS, SetupTypes.BASE])
        )),
    ]

    setup_type = SetupTypes.BASE

    def initialize_options(self):
        super(CustomCommand, self).initialize_options()

    def finalize_options(self):
        super(CustomCommand, self).finalize_options()
        assert self.setup_type in (None, SetupTypes.BASE, SetupTypes.SERVERLESS), 'Invalid setup type!'

    def prepare_requirements(self):
        requirements = os.path.join(os.getcwd(), SetupTypes.requirements(self.setup_type))
        assert os.path.exists(requirements), 'Invalid requirements path!'
        return requirements

    def prepare_install_requires(self):
        install_requires = []
        parsed_requirements = pip.req.parse_requirements(self.prepare_requirements(), session='nevermind')
        for line in parsed_requirements:
            install_requires.append(str(line.req))
        return install_requires

    def update_install_requires(self):
        self.distribution.install_requires = self.prepare_install_requires()

    def install_from_dist(self):
        pip_params = ['install', '-r', self.prepare_requirements()]
        pip.main(pip_params)


def command_factory(base_command):
    class Command(base_command, CustomCommand):
        user_options = CustomCommand.user_options + base_command.user_options
    return Command


class CustomInstall(command_factory(install)):
    def run(self):
        self.install_from_dist()
        super(CustomInstall, self).run()


class CustomDevelop(command_factory(develop)):
    def run(self):
        self.update_install_requires()
        super(CustomDevelop, self).run()


class CustomSdist(command_factory(sdist)):
    def run(self):
        self.update_install_requires()
        super(CustomSdist, self).run()


class CustomEggInfo(command_factory(egg_info)):
    def run(self):
        #TODO: Check when egg_info is fired by other class. When not fired by upstream class > run self.update_install_requires()
        #self.update_install_requires()
        super(CustomEggInfo, self).run()


def tests():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('meme_maker.tests', pattern='test_*.py')
    return test_suite


setup(name="meme-maker",
    license = "MIT",
    version='0.0.2',
    description="CLI, API and Slack bot to generate memes. Make memes not war.",
    maintainer="Jacek Szubert",
    author="Jacek Szubert",
    author_email="",
    url="https://github.com/jacekszubert/meme-maker",
    keywords="meme, memes, slack, bot, api, cli, generator",
    classifiers=["Intended Audience :: Developers",
                 "License :: OSI Approved :: BSD License",
                 "Programming Language :: Python",
                 "Topic :: Software Development :: Libraries :: Python Modules",
                 ],
    #TODO: Add option to extend install requires
    #install_requires,
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'meme-maker = meme_maker.__main__:cli',
        ]
    },
    cmdclass={
        'install': CustomInstall,
        'develop': CustomDevelop,
        'sdist': CustomSdist,
        'egg_info': CustomEggInfo
    },
    test_suite='setup.tests'
)
