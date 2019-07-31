# -*- coding: utf-8 -*-
"""Download all NSF awards from 1959 - 2019"""

# %%
from time import time
from multiprocessing.pool import ThreadPool
import os
import logging

import wget



LOG = logging.getLogger(__name__)

def download_url(url):
    """Download file from URL"""
    c_dir = os.path.join(os.getcwd(), 'download')
    try:
        wget.download(
            url, c_dir, bar=wget.bar_adaptive)  
        return '{} download success'.format(url)
    except ValueError:
        LOG.exception("Couldn't download %s", url)
        return  '{} download failure'.format(url)
# %%
# generate urls
X = range(1970, 1976)  # range of dates in nsf database
URL = """https://www.nsf.gov/awardsearch/download?DownloadFileName={}&All=true"""
URLS = []
j = 1
for i in X:
    URLS.append(URL.format(str(i)))
# %%

START = time()
RESULTS = ThreadPool(4).imap_unordered(download_url, URLS)
for path in RESULTS:
    print(path)
print('\n'+f"Total time to download: {time() - START}")
