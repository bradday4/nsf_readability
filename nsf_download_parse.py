# -*- coding: utf-8 -*-
"""Download all NSF awards from 1959 - 2019"""

# %%
from time import time
from multiprocessing.pool import ThreadPool
#import io
#import zipfile
#import os
#import requests
import sys
import wget

#from multiprocessing.pool import ThreadPool

#from clint.textui import progress


# def bar_custom(current, total, width=80):
#     """custom download bar callback"""
#     sys.stdout.write("Downloading: %d%% [%d / %d] bytes" %
#                      (current / total * 100, current, total))
#     sys.stdout.flush()


def download_url(url):
    """Download file from URL"""
    #path = os.getcwd()+r'\{}'.format(url[0])+'.zip'
    # print(url[1])
    #url = url[1]
    #r = requests.get(url, stream=True)
    wget.download(
        url, r"""C:\Users\bmday3\Documents\gitrepo\nsf_readability\test2""", bar=wget.bar_adaptive)
    return ' Success'
    # print(r.ok)
    # if r.ok:
    #z = zipfile.ZipFile(io.BytesIO(r.content))
    # z.extractall(path=os.getcwd()+r'\test')
    # with open(path, 'wb') as f:
    #     #total_length = int(r.headers.get('content-length'))
    #     for ch in r.iter_content(chunk_size=2391975):
    #         if ch:
    #             f.write(ch)


# %%
# generate urls
X = range(1970, 1976)  # range of dates in nsf database
URL = """https://www.nsf.gov/awardsearch/download?DownloadFileName={}&All=true"""
URLS = []
j = 1
for i in X:
    #URLS.append(("Event{}".format(str(j)), URL.format(str(i))))
    URLS.append(URL.format(str(i)))
    #j = j+1

# %%
START = time()
#for u in URLS:

RESULTS = ThreadPool(4).imap_unordered(download_url, URLS)
for path in RESULTS:
    print(path)

print('\n'+f"Total time to download: {time() - START}")
#ThreadPool(9).imap_unordered(download_url, urls)


# %%
