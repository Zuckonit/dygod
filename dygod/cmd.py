# coding: utf-8
import os
import sys

import click

from .dygod.core import DyGod


CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    ignore_unknown_options=True,
)

DEFAULT_HOST = 'https://www.dygod.net'


def show_movie(movies, pager=None):
    for name, movie in movies.iteritems():
        if pager:
            name = '[%s/%s] %s'%(pager.current_page_number, pager.last_page_number, name)

        click.echo(name)
        for link in movie.links:
            click.echo('\t%s' % link)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--host', default=DEFAULT_HOST, help='homepage url')
@click.pass_context
def cli(ctx, **kwargs):
    ctx.obj = kwargs


@cli.command()
@click.option('-l', '--list', default=False, help='show all categories', is_flag=True, show_default=True)
@click.option('-s', '--select', default=-1, help='choose a category', type=click.INT, show_default=True)
@click.option('-p', '--page', default=0, type=click.IntRange(min=0), help="which page", show_default=True)
@click.pass_context
def list(ctx, **kwargs):
    host = ctx.obj.get('host', DEFAULT_HOST)
    dg = DyGod(host)
    categories = dg.categories
    menus = categories.keys()

    if kwargs.get('list', False):
        for idx, name in enumerate(menus):
            click.echo('%s  %s' % (idx, name))

    page = kwargs.get('page')
    select = kwargs.get('select')
    if select != -1:
        max_select = len(categories) - 1
        select = min(kwargs.get('select'), max_select)
        category = categories[menus[select]]
        pager = category.page(page)
        movies = pager.movies
        show_movie(movies, pager=pager)


@cli.command()
@click.option('-p', '--page', default=0, type=click.INT, help="which page", show_default=True)
@click.option('-k', '--keyword', default='', help="search keyword", show_default=True)
@click.pass_context
def search(ctx, **kwargs):
    host = ctx.obj.get('host', DEFAULT_HOST)
    keyword = kwargs.get('keyword', '')
    p = kwargs.get('page', 0)
    if len(keyword) < 2:
        raise click.BadParameter('at least 2 characters for keyword')
    keyword = keyword.encode('utf-8')
    dg = DyGod(host)
    pager = dg.search(keyword).page(p)
    movies = pager.movies
    show_movie(movies, pager=pager)


if __name__ == '__main__':
    cli()
