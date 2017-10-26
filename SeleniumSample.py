from selenium import webdriver
import requests
import os
from bs4 import BeautifulSoup
import time
import threading

class ChromeBrowser(object):
    def __init__(self,chromedriver):
        self.__browser = webdriver.Chrome(chromedriver)

    def getSoup(self,url):
        try:
            self.__browser.get(url)
            for i in range(0,28000,800):   #采用for循环模拟鼠标滚轮下拉，并设置一定时间让图片缓存出来
                js = "window.scrollTo(0,"+str(i)+")"
                self.__browser.execute_script(js)
                time.sleep(0.25)
            soup = BeautifulSoup(self.__browser.page_source)
            self.__browser.quit()
            return soup
        except:
            return None

    """
    获取图片链接
    """
    def getFileList(self,soup):
        return [img["src"]  for img in soup.find_all("img",{"class":"loaded"}) ]


    """
    保存图片到指定目录
    """
    def saveImage(self,imgUrl, dir, imgname):
        if not os.path.exists(dir):
            os.makedirs(dir)
        imgname = dir + imgname
        response = requests.get(imgUrl, stream=True)
        image = response.content
        print("保存文件" + imgname)
        try:
            with open(imgname, "wb") as jpg:
                jpg.write(image)
        except IOError:
            print("IO Error\n")

    def downLoadThread(self,dir,imgs):
        index = 0
        for img in imgs:
            imgName = str(index) + ".jpg"
            self.saveImage(img, dir, imgName)
            index += 1


if __name__ == "__main__":
    chromedriver = r"./dependence/chromedriver" #selenium的驱动所在
    CONSTURL = "http://ac.qq.com/ComicView/index/id/505430/cid/" #url前面不变的部分
    startIndex = 810 #开始的章节
    endIndex = 844  #结束的章节
    offset = 17 #章节和真正url序号之间的差值
    for index in range(startIndex,endIndex):  #开始每一章节的爬虫
        mybrowser = ChromeBrowser(chromedriver) #生成一个Chrome浏览器
        dir = "./OnePieceData/" + str(index) + "/" #保存的目录
        link = CONSTURL+str(index + offset) #组合url
        page = mybrowser.getSoup(link) #获取最后经过js渲染之后的真正的页面内容
        if page == None:
            continue
        imgs = mybrowser.getFileList(page) #获取每一页的图片
        t = threading.Thread(target=mybrowser.downLoadThread, args=( dir,imgs))
        t.start()

    print("已经下载完成")
