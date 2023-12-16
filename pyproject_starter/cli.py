#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Command Line Interface Module

"""
import logging
import time

import click


@click.command()
@click.argument('number')
@click.option('-q',
              count=True,
              required=False,
              help='Decrease output level one (-q) or multiple times (-qqq).')
@click.option('-v',
              count=True,
              required=False,
              help='Increase output level one (-v) or multiple times (-vvv).')
def count(number: int, q, v):
    """
    Display progressbar while counting to the user provided integer `number`.
    """
    click.clear()
    logging_level = logging.INFO + 10 * q - 10 * v
    logging.basicConfig(level=logging_level)
    with click.progressbar(range(int(number)), label='Counting') as bar:
        for n in bar:
            click.secho(f'\n\nProcessing: {n}', fg='green')
            time.sleep(0.5)


if __name__ == '__main__':
    pass
