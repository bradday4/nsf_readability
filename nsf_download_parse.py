# -*- coding: utf-8 -*-
"""Download all NSF awards from 1959 - 2019"""

# %%
from time import time
import io
import zipfile
import os
import requests




#from multiprocessing.pool import ThreadPool

#from clint.textui import progress


def url_response(url):
    """Download file from URL"""
    #path = os.getcwd()+r'\{}'.format(url[0])+'.zip'
    #print(url[1])
    url = url[1]
    
    r = requests.get(url, stream=True)
    print(r.ok)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(path=os.getcwd()+r'\test')
    # with open(path, 'wb') as f:
    #     #total_length = int(r.headers.get('content-length'))
    #     for ch in r.iter_content(chunk_size=2391975):
    #         if ch:
    #             f.write(ch)


# %%
# generate urls
X = range(1959, 1961)  # range of dates in nsf database
URL = """https://www.nsf.gov/awardsearch/download?DownloadFileName={}&All=true"""
URLS = []
j = 1
for i in X:
    URLS.append(("Event{}".format(str(j)), URL.format(str(i))))
    #URLS.append(URL.format(str(i)))
    j = j+1

# %%
START = time()
for u in URLS:

    url_response(u)

print(f"Time to download: {time() - START}")
#ThreadPool(9).imap_unordered(url_response, urls)


#%%
