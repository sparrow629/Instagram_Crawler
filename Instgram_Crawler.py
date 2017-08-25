# -*- coding: utf-8 -*-
"""
  Author:  Sparrow
  Purpose: Crawl the single post of content from Instagram application
  Created: 2017-08-06
"""
import re
import urllib.request
import os
import traceback
from urllib.parse import quote
from bs4 import BeautifulSoup
import sys

Video = 'GraphVideo'
Image_single = 'GraphImage'
Image_set = 'GraphSidecar'

def getHtml(url):
    url = quote(url, safe="/:?=")
    try:
        page = urllib.request.urlopen(url)
        html = page.read().decode('utf-8')
        # print(html)
        return html
    except:
        traceback.print_exc()
        print('The URL you requested could not be found.')
        return 'Html'

def content_type(HTML):
    html = HTML
    isVideore_exp = r'"is_video": true'
    isVideore = re.compile(isVideore_exp)
    isVideotag = re.findall(isVideore, html)

    if isVideotag:
        print("Content is video!")
        typename = Video

    else:
        isImageSinglere_exp = r'\{"PostPage": \[\{"graphql": \{"shortcode_media": \{"__typename": "GraphImage"'
        isImageSinglere = re.compile(isImageSinglere_exp)
        isImageSingle = re.findall(isImageSinglere, HTML)

        if isImageSingle:
            print("Content is just a single Image!")
            typename = Image_single
        else:
            print("Contents are a set of Images!")
            typename = Image_set

    return typename


def findVideoUrl(HTML):
    html = HTML
    videore_raw = r'"video_url": "(https://.*?\.com/t50\.2886-16/\d*_\d*_\d*_n\.mp4)",'
    videore = re.compile(videore_raw)
    videotag = re.findall(videore, html)
    # print(videotag)
    videonum = len(videotag)
    if videonum == 1:
        videoUrl = videotag[0]
        print(videoUrl)
        return videoUrl
    elif videonum > 1:
        videoUrllist = videotag
        print(videoUrllist)
        return videoUrllist
    else:
        print('The Video url seems disappear...')
        return False


def findImageUrl_Single(HTML):
    html = HTML
    # displayre = r'"display_url": "(https://scontent-.*-.*\.cdninstagram\.com/t51\.2885-15/e35/.*_n\.jpg)", "display_resources": \[\], "is_video": false,'
    displayre = r'"display_url": "(https://.*?\.com/t51\.2885-15/.*?e35/\d*_\d*_\d*_n\.jpg)'
    imgurltagre = re.compile(displayre)
    imageurltag = re.findall(imgurltagre, html)
    # print(displayre,imageurltag)

    if imageurltag:
        imageUrl = imageurltag[0]
        print(imageUrl)
        return imageUrl
    else:
        print('The image url seems disappear...')
        return False

def findImageUrl_Set(HTML):
    html = HTML
    displayre = r'"display_url": "(https://.*_n\.jpg)", "display_resources": \[\], "is_video": false,'
    imgurllistre = re.compile(displayre)
    imageurllist_raw = re.findall(imgurllistre, html)
    if imageurllist_raw:
        # imglistre_exp = r'"display_url": "(https://scontent-.*?\d-\d\.cdninstagram\.com/t51\.2885-15/e35/\d*_\d*_\d*_n\.jpg)'
        imglistre_exp = r'"display_url": "(https://.*?\.com/t51\.2885-15/.*?e35/\d*_\d*_\d*_n\.jpg)'
        imglistre = re.compile(imglistre_exp)
        imageurllists = re.findall(imglistre, imageurllist_raw[0])
        # print(imglistre, imageurllist_raw[0], '\n\n', imageurllists)

        if imageurllists :
            imageurllist = list(set(imageurllists))
            print(imageurllist)
            return imageurllist
        else:
            print('The set of image urls seems disappear...')
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


def DownloadVideo(videourl, postname):
    VideoUrl = videourl
    VideoName = postname

    if VideoUrl and VideoName:
        path = 'InstgramVideo/'
        if not os.path.exists(path):
            os.makedirs(path)

        target = path + '%s.mp4' % VideoName
        print("Downloading Video %s \n" % target)
        try:
            urllib.request.urlretrieve(VideoUrl, target, progress_report)
        except:
            print("The Video seems disappear...")

def DownloadImage_Single(imageurl, postname):
    ImgUrl = imageurl
    ImgName = postname

    if ImgUrl and ImgName:
        path = 'InstgramImage/'
        if not os.path.exists(path):
            os.makedirs(path)

        target = path + '%s.jpg' % ImgName
        print("Downloading %s \n" % target)
        try:
            urllib.request.urlretrieve(ImgUrl, target, progress_report)
        except:
            print("The image seems could not be downloaded...")

def DownloadImage_set(imageurllist, postname):
    ImageUrlList = imageurllist
    PostName = postname

    if ImageUrlList and PostName:
        path = 'InstgramImage/'
        if not os.path.exists(path):
            os.makedirs(path)

        count = 0
        for imageurl in ImageUrlList:
            count += 1
            target = path + '%s_%d.jpg' % (PostName, count)
            print("Downloading %s \n" % target)
            try:
                urllib.request.urlretrieve(imageurl, target, progress_report)
            except:
                print("The %s image seems could not be downloaded..." % count)


def progress_report(blocknum, blocksize, totalsize):
    #blocknum: 已经下载的数据块; blocksize: 数据块的大小; totalsize: 远程文件的大小
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent >= 100:
        percent = 100.0
    sys.stdout.write("\r" + "Downloading block %d, %d/%d, ===> %.2f%%" % (blocknum, blocknum*blocksize, totalsize, percent))
    sys.stdout.flush()

def DownloadContent(url):
    HTML = getHtml(url)
    ContentType = content_type(HTML)

    if ContentType == Video:
        VideoUrl = findVideoUrl(HTML)
        VideoName = getPostname(url)

        if not isinstance(VideoUrl, list):
            DownloadVideo(VideoUrl, VideoName)
        else:
            VideoNumber = len(VideoUrl)
            print("There are %d videos in this post" % VideoNumber)
            for count in range(VideoNumber):
                videoname = VideoName + '_%d' % count
                DownloadVideo(VideoUrl[count], videoname)
        return VideoUrl
    elif ContentType == Image_single:
        ImageUrl = findImageUrl_Single(HTML)
        ImageName = getPostname(url)
        DownloadImage_Single(ImageUrl, ImageName)
        return ImageUrl
    else:
        ImageUrlList = findImageUrl_Set(HTML)
        PostName = getPostname(url)
        DownloadImage_set(ImageUrlList, PostName)
        return ImageUrlList

def CallbackAPI_URL(url):
    HTML = getHtml(url)
    ContentType = content_type(HTML)

    if ContentType == Video:
        VideoUrl = findVideoUrl(HTML)
        return VideoUrl

    elif ContentType == Image_single:
        ImageUrl = findImageUrl_Single(HTML)
        return ImageUrl
    else:
        ImageUrlList = findImageUrl_Set(HTML)
        return ImageUrlList


def main():
    print('''
                    ---------------------------------
                       Welcome to Instgram Crawler!
                    ---------------------------------
                    Author:  Sparrow
                    Purpose: downloading images and videos from any Tumblr once.
                    Created: 2017.08.06
                    Version: 1.6
                    Manual: https://github.com/sparrow629/Instagram_Crawler
                    署名-非商业使用-禁止演绎 (by-nc-nd)：
                    ''')
    select = 'N'
    post_reg = r'https://www.instagram.com/p/.*?'
    while not (select == 'Y'):

        URL = input('Input url: ')
        if re.match(post_reg, URL):
            DownloadContent(URL)
        else:
            print("The url seems not to be a post... Please input again!")

        select = input("\nDo you want to Quit? [Y/N]")

if __name__ == '__main__':
    main()

    # url1_multi = 'https://www.instagram.com/p/BXZyl4GBhXy/'
    # url_video = 'https://www.instagram.com/p/BXMc-NXhwaL/'
    # url_video1 = 'https://www.instagram.com/p/BXPI0yfAHBz/'
    # url_videoset = 'https://www.instagram.com/p/BXcvKDwB30E/'
    # url2_single = 'https://www.instagram.com/p/BXbuLwlFL7Q/'
    # url3_single = 'https://www.instagram.com/p/BXUSWaYgc_y/'
    # url4_multi = 'https://www.instagram.com/p/BXaI4Dkhhv5/'
    # url5_multi = 'https://www.instagram.com/p/BW8-SvFBqge/?taken-by=ssovely1024'
    
    # ContentUrl = CallbackAPI_URL(url1_multi)
    # print(ContentUrl)
    # HTML = getHtml(url_videoset)
    # Videourl = findVideoUrl(HTML)
    # DownloadContent(url_videoset)
