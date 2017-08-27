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
Type_Mixed = [Video, Image_set]

def getHtml(url):
    url = quote(url, safe="/:?=")
    try:
        page = urllib.request.urlopen(url)
        html = page.read().decode('utf-8')
        # print(html)
        return html
    except:
        # traceback.print_exc()
        print('The URL you requested could not be found.')
        return 'Html'

def content_type(HTML):
    html = HTML
    TypeNamere_exp = r'"__typename": "(GraphImage|GraphSidecar|GraphVideo)"'
    TypeNamere = re.compile(TypeNamere_exp)
    TypeNametags = re.findall(TypeNamere, html)
    # print(TypeNametags)

    if TypeNametags:
        if TypeNametags[0] == Video:
            print("Content is a single video!")
            typename = Video

        elif TypeNametags[0] == Image_single:
            print("Content is just a single Image!")
            typename = Image_single
        else:
            TypeNametag = list(set(TypeNametags))
            TypeNametag.remove('GraphSidecar')
            # print(TypeNametag)
            mix = len(TypeNametag)
            if mix == 1:
                if TypeNametags[0] == Video:
                    print("Content is a set of videos!")
                    typename = Video

                elif TypeNametags[0] == Image_set:
                    print("Content is a set of Images!")
                    typename = Image_set
            else:
                print("Contents are a set of contents including video and image!")
                typename = Type_Mixed

    else:
        print("No Contents")
        typename = None

    return typename


def findVideoUrl(HTML):
    html = HTML
    videore_raw = r'"video_url": "(https://.*?\.com/t50\.2886-16/\d*_\d*_\d*_n\.mp4)",'
    videore = re.compile(videore_raw)
    videotag = re.findall(videore, html)
    # print(videotag)
    videonum = len(videotag)
    if videonum == 1:
        videoUrl = videotag
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
        imageUrl = imageurltag
        print(imageUrl)
        return imageUrl
    else:
        print('The image url seems disappear...')
        return False

def findImageUrl_Set(HTML):
    html = HTML
    displayre = r'"display_url": "(https://.*?\.com/t51\.2885-15/.*?e35/\d*_\d*_\d*_n\.jpg)'
    imgurllistre = re.compile(displayre)
    imageurllists = re.findall(imgurllistre, html)

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
    ImgUrl = imageurl[0]
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
            print("\n\nDownloading %s \n" % target)
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
        VideoNumber = len(VideoUrl)

        if VideoNumber == 1:
            DownloadVideo(VideoUrl[0], VideoName)
        else:
            print("There are %d videos in this post" % VideoNumber)
            for count in range(VideoNumber):
                videoname = VideoName + '_%d' % count
                DownloadVideo(VideoUrl[count], videoname)

    elif ContentType == Image_single:
        ImageUrl = findImageUrl_Single(HTML)
        ImageName = getPostname(url)
        DownloadImage_Single(ImageUrl, ImageName)

    elif ContentType == Image_set:
        ImageUrlList = findImageUrl_Set(HTML)
        PostName = getPostname(url)
        DownloadImage_set(ImageUrlList, PostName)

    elif ContentType == Type_Mixed:
        VideoUrl = findVideoUrl(HTML)
        VideoName = getPostname(url)
        VideoNumber = len(VideoUrl)

        if VideoNumber == 1:
            DownloadVideo(VideoUrl[0], VideoName)
        else:
            print("There are %d videos in this post" % VideoNumber)
            for count in range(VideoNumber):
                videoname = VideoName + '_%d' % count
                DownloadVideo(VideoUrl[count], videoname)

        print("\nFinishing download video, then download images")
        ImageUrlList = findImageUrl_Set(HTML)
        DownloadImage_set(ImageUrlList, VideoName)

    else:
        print("It seems no content or to ba a post of private account which cannot be downloaded without login! ")


def CallbackAPI_URL(url):
    HTML = getHtml(url)
    ContentType = content_type(HTML)

    if ContentType == Video:
        VideoUrl = findVideoUrl(HTML)
        result =  VideoUrl
    elif ContentType == Image_single:
        ImageUrl = findImageUrl_Single(HTML)
        result = ImageUrl
    elif ContentType == Image_set:
        ImageUrlList = findImageUrl_Set(HTML)
        result = ImageUrlList
    elif ContentType == Type_Mixed:
        result = []
        VideoUrl = findVideoUrl(HTML)
        result += VideoUrl
        ImageUrlList = findImageUrl_Set(HTML)
        result += ImageUrlList
    else:
        result = None
    print(result)
    return result


def main():
    print('''
                    ---------------------------------
                       Welcome to Instagram Crawler!
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
            # CallbackAPI_URL(URL)
        else:
            print("The url seems not to be a post... Please input again!")

        select = input("\nDo you want to Quit? [Y/N]")

if __name__ == '__main__':
    main()
