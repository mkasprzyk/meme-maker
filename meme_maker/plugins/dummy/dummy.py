#!/usr/bin/env python
from pprint import pprint


def run(context):
    context.logger.info('Received context: {}'.format(context.to_dict()))
    return context
