#!/usr/bin/env python

# -*- coding: utf-8 -*-
__author__ = 'itmard'

import click


@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path(), required=False)
@click.option('--fix_persian', is_flag=True, help='Decode Unicode and fix issues with Persian')
@click.option('--shift')
def cli(input, output, fix_persian, shift):
    '''
        SubFixer a subtitle fixer for command line
        using Python and click module.

    '''
    if input[-4:] not in ('.srt', '.SRT'):
        click.echo('%s is not a srt file.' % click.format_filename(input))
        exit()

    