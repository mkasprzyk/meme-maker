#!/usr/bin/env python

import click
import sys
import logging

from PIL import Image, ImageDraw, ImageFont

from meme import Meme

LOG_FORMAT = "%(levelname)9s [%(asctime)-15s] %(name)s - %(message)s"
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--debug', is_flag=True)
@click.option('--meme', '-m', help='meme template to be used')
@click.option('--url', '-u', help='image url')
@click.argument('text', nargs=-1)
def cli(debug, meme, url, text):
    template = meme
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
    logger = logging.getLogger('meme')
    if debug:
        logger.info('Identified parameters:')
        logger.info('%6s:   %s' % ('url', url))
        logger.info('%6s:   %s' % ('template', template))
        logger.info('%6s:   %s' % ('text', text))

    meme = Meme(logger, template, url, text)
    #meme.make_meme('/tmp')
    meme.make_meme('kektest')


if __name__ == '__main__':
    cli()
