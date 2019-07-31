# -*- coding: utf-8 -*-
"""Download all NSF awards from 1959 - 2019"""

from time import time
from multiprocessing.pool import ThreadPool
import os
import logging
import argparse
import wget

LOG = logging.getLogger(__name__)
PARSER = argparse.ArgumentParser(description='Path to Directory')
PARSER.add_argument('--directory', nargs='?')
PARSER.add_argument('--dates', nargs=2, type=int, default=[1959, 1960])

def main():
    '''main function'''
    global PATH
    args = PARSER.parse_args()
    if args.directory:
        PATH = args.directory
    else:
        PATH = os.getcwd()

    urls_2_retrieve = generate_urls(args.dates)
    start = time()
    results = ThreadPool(4).imap_unordered(download_url, urls_2_retrieve)
    print('\n'+f"Total time to download: {time() - start}")

def download_url(url):
    """Download file from URL"""
    #c_dir = os.path.join(os.getcwd(), 'download')
    try:
        wget.download(
            url, PATH, bar=wget.bar_adaptive) 
        return '{} download success'.format(url)
    except ValueError:
        LOG.exception("Couldn't download %s", url)
        return  '{} download failure'.format(url)

def generate_urls(year_range):
    '''
    generate urls
    '''
    beggining_year, end_year = year_range
    end_year = end_year+1
    # check years are within range
    if 1959 <= beggining_year <= 2019 and 1959 <= end_year <= 2019 and beggining_year <= end_year:
        years = range(beggining_year, end_year)
    else:
        raise ValueError('Values not within range or out of order')
    url_base = """https://www.nsf.gov/awardsearch/download?DownloadFileName={}&All=true"""
    urls_2_retrieve = [url_base.format(str(i)) for i in years]
    return urls_2_retrieve

if __name__ == '__main__':
    main()
