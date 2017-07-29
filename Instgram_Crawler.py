# -*- coding: utf-8 -*-
"""
  Author:  Sparrow
  Purpose: downloading one entire blog from Tumblr once.
  Created: 2017-1.1
"""
import re
import urllib.request
import os
import traceback
from urllib.parse import quote
from bs4 import BeautifulSoup

def getHtml(url):
    url = quote(url, safe="/:?=")
    try:
        page = urllib.request.urlopen(url)
        html = page.read()
        # print(html)
        return html
    except:
        traceback.print_exc()
        print('The URL you requested could not be found in Module image')
        return 'Html'

def findImageUrl(url):
    html = getHtml(url)
    Soup = BeautifulSoup(html, 'lxml')
    tag = Soup.select('#react-root > section > main > div > div > article > div._h5v2a._kqf30 > div > div > div._jjzlb > img')

    if tag[0]:
        imageUrl = tag[0].get('src')
        # print(imageUrl)
        # print(tag)
        return imageUrl
    else:
        print('The image url seems disappear...')
        return False

def getPostname(posturl):
    reg = r'https://www.instagram.com/p/(.*)/'
    postnameRe = re.compile(reg)
    postnames = re.findall(postnameRe, posturl)
    if postnames:
        print(postnames[0])
        return postnames[0]
    else:
        print('Lost postname...')
        return False

def DownloadImage(url):
    ImgUrl = findImageUrl(url)
    ImgName = getPostname(url)

    if ImgUrl and ImgName:
        path = 'InstgramImage/'
        if not os.path.exists(path):
            os.makedirs(path)

        target = path + '%s.jpg' % ImgName
        print("Downloading %s \n" % target)
        try:
            urllib.request.urlretrieve(ImgUrl, target)
        except:
            print("The image seems disappear...")

if __name__ == '__main__':
    url = 'https://www.instagram.com/p/BW6lCSchA94/'

    DownloadImage(url)