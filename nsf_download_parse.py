import os

import requests

from time import time

from multiprocessing.pool import ThreadPool

from clint.textui import progress


def url_response(url):

    path, url = url

    r = requests.get(url, stream=True)

    with open(path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for ch in progress.bar(r.iter_content(chunk_size=2391975), expected_size=(total_length/1024) + 1):
            if ch:
                f.write(ch)

#%%
# generate urls
x = range(1959, 1961)  # range of dates in nsf database
url = """https://www.nsf.gov/awardsearch/download?DownloadFileName={}&All=true"""
urls = []
j = 1
for i in x:
    #urls.append(("Event{}".format(str(j)), url.format(str(i))))
    urls.append(url.format(str(i)))
    j = j+1
#%%
start = time()
for u in urls:

    url_response(u)

print(f"Time to download: {time() - start}")
#ThreadPool(9).imap_unordered(url_response, urls)
