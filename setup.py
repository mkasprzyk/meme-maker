#!/usr/bin/env python
from setuptools import setup, find_packages
from setuptools.command.install import install
import pip

import os
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

class CustomInstall(install):
    requirements_base = 'requirements/base.txt'

    def prepare_requirements(self):
        requirements = os.path.join(os.getcwd(), self.requirements_base)
        return requirements

    def install_from_dist(self):
        pip_params = ['install', '-r', self.prepare_requirements()]
        pip.main(pip_params)

    def run(self):
        self.install_from_dist()
        install.run(self)


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
            'meme-maker = meme_maker.__main__:handler',
        ]
    },
    cmdclass={
        'install': CustomInstall
    },
)
