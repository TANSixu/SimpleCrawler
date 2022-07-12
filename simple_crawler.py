# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 16:54:24 2022

@author: Tan Sixu
"""

import requests
from bs4 import BeautifulSoup
import warnings
from jparser import PageModel
import argparse
import time
import os
from tqdm import tqdm
import chardet

###### set search keyword #######

kw = "Hello world!"

#################################



# used as default dir name
time_stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime()) 

parser = argparse.ArgumentParser(description="Set search args")
# parser.add_argument('keyword', type=str, help="keyword for search")
parser.add_argument("-n", "--num", default=1, type=int ,help="number of pages to craw")
parser.add_argument("-d", "--dir_name", default=time_stamp, type=str, help="directory name to save the crawled files")

args = parser.parse_args()

pg_size = 10
pg_num = args.num
dir_name = args.dir_name


headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}


def extract_page_urls(soup):
    """
    This function extract urls on a page from search engine.

    Parameters
    ----------
    soup : BeautifulSoup
        soup with prepared html.

    Returns
    -------
    result: dictionary {name: url}

    """
    result = {}
    for itm in soup.find_all("a"):
        if itm.find("h3") is None:
            # no title, possibly an ad
            continue
        
        name = itm.find("h3").text
        url = itm['href']
        result[name] = url
    return result

def extract_urls(kw, pg_limit):
    """
    This function extract urls from search engine result.

    Parameters
    ----------
    kw: search key words

    pg_limit: Limit of pages number

    Returns
    -------
    urls: dictionary {name: url}
    """
    urls = {}
    for pg_start in range(0, pg_limit * pg_size, pg_size):
        kv = {"q": kw, "start": pg_start}
        html = requests.get("https://www.google.com/search", params=kv, headers=headers)
        if html.status_code//100 != 2:
            warnings.warn("Potential problem with the website")
        soup = BeautifulSoup(html.text, 'html.parser')
        cur_pg_urls = extract_page_urls(soup)
        urls.update(cur_pg_urls)
    return urls

def extract_content(html):
    """
    This function extract content from a html file.

    Parameters
    ----------
    html: str, html file

    Returns
    -------
    content: extracted content, with format: 
    
    Titile

    Main content
    """
    pm = PageModel(html)
    rs = pm.extract()
    title = "Default title"
    try:
        title = rs['title'].encode('GB2312')
    except Exception:
        warnings.warn("potential problem with encoding")
    content = title + "\n\n"
    for x in rs['content']:
        if x['type'] == 'text':
            try:
                content += x['data'].encode('GB2312')
            except Exception:   
                warnings.warn("potential problem with encoding")
    return content


# Main
r = extract_urls(kw, pg_num)
cnt = 0
os.mkdir(dir_name)
with tqdm(len(r)) as bar:
    bar.set_description("crawling...")
    for k, v in r.items():
        try:
            result = requests.get(v, headers=headers)
            content = extract_content(result.text)
            fname = dir_name + "@" + str(cnt) + ".txt"
            path = os.path.join(os.getcwd(), dir_name, fname)
            with open(path, 'w') as file:
                file.write(content)
        except Exception:
            warnings.warn("potential error with file "+str(cnt))
        bar.update(1)
        cnt += 1



