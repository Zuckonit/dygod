#!/usr/bin/env python
#coding: utf-8

"""
    dygod wrapper for fucking the ads.

    author: Mocker
    licence: MIT
    ~~~~~~~~
    dygod.py
"""

import re
import sys

PY3 = sys.version > '3'
if PY3:
    from urllib.parse import urljoin, urlparse as urlsplit
    from urllib.parse import urlencode
else:
    from urlparse import urljoin, urlsplit
    from urllib import urlencode

from functools import partial

import requests
requests.packages.urllib3.disable_warnings()
from fake_useragent import UserAgent


REGEX_CATEGORY = re.compile(r'<a href="(/.*?)"?>(.+)?</a></li><li>')
REGEX_SEARCH = re.compile(
    r'<a href="(.+?)" class="ulink" title="(.+?)">.+?</a>')
REGEX_PAGES = re.compile(
    r'<a href="(/e/search/result/searchid-.+?)">([\d\w]+?)</a>')
REGEX_TOTAL = re.compile(r'<b>(\d+?)</b>[\s\S]*</a>')
REGEX_LAST = re.compile(r'<a href="/e/search/result/(.+?)">尾页</a></div>')
REGEX_DOWNLOAD_URL = re.compile(r'<a href="(ftp://.+?)">')
UA = UserAgent().random


__all__ = [ 'DyGod' ]


def lazy_property(fn):
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazyprop(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return _lazyprop


class DyMixin(object):

    def __init__(self, host):
        super(DyMixin, self).__init__()
        self.host = host
        self.api_search_base = urljoin(self.host, '/e/search/')
        self.__session = requests.Session()

    def request(self, url, method, **kwargs):
        return_object = kwargs.pop('return_object', False)
        method = method.lower()
        headers = kwargs.get('headers', {})
        headers.setdefault('user-agent', UA)
        urlpart = urlsplit(self.host)
        headers.setdefault('host', urlpart.netloc)
        headers.setdefault('origin', self.host)
        headers.setdefault('referer', self.host)
        urlpart.scheme == 'https' and kwargs.setdefault('verify', False)
        request_func = getattr(self.__session, method)
        resp = request_func(url, **kwargs)
        return resp if return_object else self.gbk2utf8(resp.content)

    def request_get(self, url, **kwargs):
        return self.request(url, 'get', **kwargs)

    def request_post(self, url, **kwargs):
        return self.request(url, 'post', **kwargs)

    @staticmethod
    def utf82gbk(utf8, errors='ignore'):
        if PY3:
            return utf8.encode('gbk', errors)
        else:
            return utf8.decode('utf-8', errors).encode('gbk', errors)

    @staticmethod
    def gbk2utf8(gbk, errors='ignore'):
        if PY3:
            return gbk.decode('utf-8', errors)
        else:
            return gbk.decode('gbk', errors).encode('utf-8', errors)


class DyGod(DyMixin):

    def __init__(self, host):
        super(DyGod, self).__init__(host)
        self.host = host

    @lazy_property
    def html(self):
        return self.request_get(self.host)

    @lazy_property
    def categories(self):
        cates = REGEX_CATEGORY.findall(self.html)
        return {
            c[1]: Category(
                self.host, 
                c[1],
                c[0].rstrip('index.html')
            )
            for c in cates
        }

    @lazy_property
    def search_url(self):
        return urljoin(self.host, '/e/search/index.php')

    def select(self, category):
        return self.categories.get(category)

    def __search_post(self, url, keyword):
        gbk_submit = self.utf82gbk('立即搜索')
        gbk_keyword = self.utf82gbk(keyword)
        params = {
            'show': 'title',
            'tempid': 1,
            'keyboard': gbk_keyword,
            'Submit': gbk_submit
        }
        headers = {
            'upgrade-insecure-requests': '1',
            'content-type': 'application/x-www-form-urlencoded',
            'dnt': '1',
            'cache-control': 'max-age=0',
        }
        resp = self.request_post(
            url,
            data=urlencode(params),
            headers=headers,
            return_object=True,
            allow_redirects=False
        )
        return resp

    def search(self, keyword=''):
        if len(keyword) < 2:
            return {}
        resp = self.__search_post(self.search_url, keyword=keyword)
        location = resp.headers.get('location')
        first_page_url = urljoin(self.api_search_base, location)
        resp = self.__search_post(first_page_url, keyword=keyword)
        html = self.gbk2utf8(resp.content)
        html2 = '\n'.join(html.split('&nbsp;'))
        s = REGEX_PAGES.findall(html2)
        if s:
            page_url = s[0][0]
            page_url_prefix = '-'.join(page_url.split('.', 2)[0].split('-')[:-1])
            return Pager(self.host, page_url_prefix, 0)
        else:
            return Pager(
                self.host, location, 0,
                search_urlbase=self.api_search_base,
                get_page_url=self.get_page_url,
                get_total_movies=self.get_total_movies,
                get_last_page_number=self.get_last_page_number
            )

    def get_page_url(self, urlbase, page_url_prefix, current_number):
        return urljoin(urlbase, page_url_prefix)
    
    def get_total_movies(self, html):
        return -1
    
    def get_last_page_number(self, html):
        return 0


class Category(DyMixin):

    regex_total = re.compile(r'nbsp;总数(\d+?)&nbsp;')
    regex_last_page = re.compile(r"<a href='.+?index_(\d+?)\.html'>尾页</a>")

    def __init__(self, host, name, url):
        super(Category, self).__init__(host)
        self.host = host
        self.name = name
        self.category_url = url
        self.url = urljoin(self.host, url) 

    @lazy_property
    def html(self):
        return self.request_get(self.category_url)

    def __getattr__(self, name):
        page_url_prefix = urljoin(self.category_url, 'index')
        p = Pager(
            self.host, page_url_prefix, 0, 
            get_page_url=self.get_page_url,
            get_total_movies=self.get_total_movies,
            get_last_page_number=self.get_last_page_number
        )
        return getattr(p, name)
    
    def get_page_url(self, urlbase, page_url_prefix, current_number):
        if current_number <= 1:
            path = '{0}.html'.format(page_url_prefix)
        else:
            path = '{0}_{1}.html'.format(page_url_prefix, current_number)
        return urljoin(urlbase, path)
    
    def get_total_movies(self, html):
        return int(self.regex_total.findall(html)[0])
    
    def get_last_page_number(self, html):
        return int(self.regex_last_page.findall(html)[0])
        


class Pager(DyMixin):

    def __init__(self, host, page_url_prefix, current_number, 
            search_urlbase=None,
            get_page_url=None, get_total_movies=None, get_last_page_number=None):
        super(Pager, self).__init__(host)
        self.host = host
        self.search_urlbase = search_urlbase or self.host
        self.page_url_prefix = page_url_prefix

        self.get_page_url = self.choose_getter(get_page_url, self.default_get_page_url)
        self.get_total_movies = self.choose_getter(get_total_movies, self.default_get_total_movies)
        self.get_last_page_number = self.choose_getter(get_last_page_number, self.default_get_last_page_number)
        self.__current_page_number = current_number
    
    @staticmethod
    def choose_getter(getter, default_getter):
        return getter if callable(getter) else default_getter

    @staticmethod
    def default_get_page_url(urlbase, page_url_prefix, current_number):
        path = '-'.join([page_url_prefix, str(current_number)]) + '.html'
        return urljoin(urlbase, path)

    @property
    def current_page_number(self):
        return self.__current_page_number

    @lazy_property
    def html(self):
        page_url = self.get_page_url(self.search_urlbase, self.page_url_prefix, self.current_page_number)
        return self.request_get(page_url)

    @lazy_property
    def total(self):
        return self.get_total_movies(self.html)
    
    def default_get_total_movies(self, html):
        return int(REGEX_TOTAL.findall(html)[0])

    @lazy_property
    def last_page_number(self):
        return self.get_last_page_number(self.html)

    @staticmethod
    def get_html2(html):
        return '\n'.join(html.split('&nbsp;'))

    def default_get_last_page_number(self, html):
        html2 = self.get_html2(html)
        page_string = REGEX_LAST.findall(html2)[0]
        # searchid-112149-page-108.html
        page = page_string.split('-')[-1].rstrip('.html')
        return int(page)

    def has_next(self, n=1):
        return self.__current_page_number + n <= self.last_page_number

    def has_prev(self, n=1):
        return self.__current_page_number - n >= 0

    def page(self, n):
        return Pager(self.host, self.page_url_prefix, n,
            search_urlbase=self.search_urlbase,
            get_page_url=self.get_page_url, 
            get_total_movies=self.get_total_movies, 
            get_last_page_number=self.get_last_page_number
        )
    
    def next(self, n=1):
        if not self.has_next(n):
            return
        self.__current_page_number += n
        return self.page(self.current_page_number)

    def prev(self, n=1):
        if not self.has_prev(n):
            return
        self.__current_page_number -= n
        return self.page(self.current_page_number)

    @lazy_property
    def html2(self):
        return self.get_html2(self.html)

    @lazy_property
    def movies(self):
        movies = REGEX_SEARCH.findall(self.html2)
        return {m[1]: Movie(self.host, m[1], m[0]) for m in movies}



class Movie(DyMixin):

    def __init__(self, host, name, url):
        super(Movie, self).__init__(host)
        self.name = name
        self.url = urljoin(host, url)

    @lazy_property
    def html(self):
        return self.request_get(self.url)
    
    @lazy_property
    def profile(self):
        #TODO
        pass
    
    @lazy_property
    def links(self):
        return list(sorted(REGEX_DOWNLOAD_URL.findall(self.html)))

    @lazy_property
    def category(self):
        #TODO
        pass

    @lazy_property
    def score(self):
        pass


if __name__ == '__main__':
    dg = DyGod('https://www.dygod.net')
    print dg.categories
