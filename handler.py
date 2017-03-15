<<<<<<< HEAD
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
=======
#!/usr/bin/env python

import json
import logging
import os
import requests

from urlparse import parse_qs
from meme_maker.meme import Meme

LOG_FORMAT = "%(levelname)9s [%(asctime)-15s] %(name)s - %(message)s"


def get_value_from_command(args, key):
    try:
        value = next(arg for arg in args if arg.startswith('%s:' % key))
        args.remove(value)
        return ':'.join(value.split(':')[1:]), args
    except:
        return None, args

def response(text, response_url=None):
    data = {
        "response_type": "in_channel",
        "text": text
    }
    headers = {'Content-Type': 'application/json'}

    if response_url:
        r = requests.post(response_url, data=json.dumps(data), headers=headers)
        return r.text

    return {
        'statusCode': '200',
        'body': json.dumps(data),
    }.update(headers)


def handler(event, context):
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
    logger = logging.getLogger('meme')

    print event

    bucket = os.environ['bucket']
    params = parse_qs(event['body'])
    command = params['text'][0].split(' ')
    response_url = params['response_url'][0]
    user_name = params['user_name'][0]

    url, command = get_value_from_command(command, 'url')
    template, command = get_value_from_command(command, 'meme')
    text = ' '.join(command)

    if not template and not url:
        return response('no parameters no meme no kek')

    meme = Meme(logger, template, url, text)
    meme_path = meme.make_meme(bucket)

    meme_url = 'https://{}.s3.amazonaws.com/{}'.format(bucket, meme_path)
    response_text = "@{}: here's your meme: {}".format(user_name, meme_url)

    return response(response_text, response_url)
>>>>>>> 3c76a3cf64e27dac3d9f84c31f69fa04c02b80e4
