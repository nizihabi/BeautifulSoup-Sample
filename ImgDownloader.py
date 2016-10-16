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

#htmlSoup = getSoup("http://tieba.baidu.com/p/4809230615")
#imgs = getFileList(htmlSoup,**{"class":"BDE_Image"})
#saveImg("./imgData",imgs)

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.933.400 QQBrowser/9.4.8699.400",
    "Cookie":"cuid=1097120620; pac_uid=1_1493982441; tvfe_boss_uuid=a681e78506f4f48a; RK=2nEWCbNjO1; pgv_pvi=3598561280; o_cookie=1493982441; ptcz=9258c903a08880c4ce0d71f4de8eb68e054f516954968aa6a6204a11d418bf13; pt2gguin=o1493982441; theme=dark; roastState=1; pgv_si=s8046535680; pc_userinfo_cookie=; ts_refer=hanhuazu.cc/cartoon/post; readRecord=%5B%5B505430%2C%22%E6%B5%B7%E8%B4%BC%E7%8E%8B%2F%E8%88%AA%E6%B5%B7%E7%8E%8B%22%2C828%2C%22%E7%AC%AC811%E8%AF%9D%20ROKO%22%2C811%5D%5D; readLastRecord=%5B%5D; pgv_info=ssid=s6644996197; pgv_pvid=4115647938; ts_uid=9386960475",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection":"keep-alive",
    "Host":"ac.qq.com",
    "Accept-Encoding":"gzip, deflate, sdch"
    }

opener = request.build_opener()
opener.addheaders = [header]
data = opener.open("http://ac.qq.com/ComicView/index/id/505430/cid/829").read()
print(data)

