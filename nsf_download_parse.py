# -*- coding: utf-8 -*-
"""Download all NSF awards from 1959 - 2019"""

from time import time
from multiprocessing.pool import Pool
import os
import logging
import argparse
import copyreg
import types
import wget

LOG = logging.getLogger(__name__)
PARSER = argparse.ArgumentParser(description='Path to Directory')
PARSER.add_argument('--directory', nargs='?')
PARSER.add_argument('--dates', nargs=2, type=int, default=[1969, 1974])

def _pickle_method(method):
    class_self = method.im_class if method.im_self is None else method.im_self
    return getattr, (class_self, method.im_func.func_name)

copyreg.pickle(types.MethodType, _pickle_method)

class UrlGetter:
    '''
    object for downloading from URL
    '''
    def __init__(self, path):
        self.path = path
        self.urls_2_retrieve = []
        self.pool = Pool(4)

    def __iter__(self):
        if not self.urls_2_retrieve:
            raise StopIteration('Empty List : urls_2_retrieve cannot be empty')
        return iter(self.urls_2_retrieve)

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def download_url(self, url):
        """Download file from URL"""
        #c_dir = os.path.join(os.getcwd(), 'download')
        try:
            wget.download(
                url, self.path, bar=wget.bar_adaptive)
            return '{} download success'.format(url)
        except ValueError:
            LOG.exception("Couldn't download %s", url)
            return  '{} download failure'.format(url)

    def run(self):
        '''
        run pickled method
        '''
        success = self.pool.map(self.download_url, self)
        return success

    def generate_urls(self, year_range):
        '''
        generate urls
        '''
        beggining_year, end_year = year_range
        end_year = end_year+1
        # check years are within range
        if 1959 <= beggining_year <= 2020 and \
            1959 <= end_year <= 2020 and \
            beggining_year <= end_year:

            years = range(beggining_year, end_year)
        else:
            raise ValueError('Values not within range or out of order')
        url_base = """https://www.nsf.gov/awardsearch/download?DownloadFileName={}&All=true"""
        self.urls_2_retrieve = [url_base.format(str(i)) for i in years]
        return self.urls_2_retrieve

def main():
    '''main function'''
    args = PARSER.parse_args()
    if args.directory:
        url_object = UrlGetter(args.directory)
    else:
        url_object = UrlGetter(os.getcwd())

    url_object.generate_urls(args.dates)
    start = time()
    url_object.run()
    # ThreadPool(4).imap_unordered(url_object.download_url,
    #                              url_object)
    print('\n'+f"Total time to download: {time() - start}")

if __name__ == '__main__':
    main()
