import logging

from meme_maker.meme import Meme
from meme_maker.cli import LOG_FORMAT

logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
logger = logging.getLogger('meme_handler')


def meme_handler(event, context):
    params = event.get('text').split(' ')

    if len(params) >= 2:

        template_or_url = params[1]
        #TODO: urlparse instead of dumb string check
        if template_or_url.startswitch('http'):
            template = None
            url = template_or_url
        else:
            template = template_or_url
            url = None

        text = ' '.join(params[1:])

    else:
        return 'Invalid meme-maker params. Try: /meme [template or url] [text...]'

    meme = Meme(logger, template, url, text)
    #meme.make_meme()
    #TODO: return link to meme @ S3