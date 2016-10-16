from urllib import request
import re
from bs4 import BeautifulSoup
import os

def getSoup(url,**kw):
    if len(kw) > 0:
        pagerequest = request.Request(url,data=kw[data],headers=kw[header])
    else:
        pagerequest = request.Request(url)
    page = request.urlopen(pagerequest).read()
    soup = BeautifulSoup(page)
    return soup

def getFileList(soup,tag="img",**kwargs):
    filelist=[]
    for img in soup.find_all(tag, kwargs):
        imgsrc = img["src"]
        filelist.append(imgsrc)
    return filelist

def saveImg(dir,imgLinkList):
    imgIndex = 0
    if not os.path.exists(dir):
        os.makedirs(dir)
    for links in imgLinkList:
        try:
            filename = dir + "/" + str(imgIndex) + ".jpg"
            request.urlretrieve(links,filename)
            imgIndex+=1
        except:
            continue

htmlSoup = getSoup("http://tieba.baidu.com/p/4809230615")
imgs = getFileList(htmlSoup,**{"class":"BDE_Image"})
saveImg("./imgData",imgs)



