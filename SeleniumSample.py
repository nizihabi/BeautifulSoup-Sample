"""
使用Selenium模拟浏览器爬取动态页面，对腾讯动漫中海贼王的一些章节进行爬取
"""
from selenium import webdriver
import requests
import os
from bs4 import BeautifulSoup
import time

class ChromeBrowser(object):
    def __init__(self,chromedriver):
        self.__browser = webdriver.Chrome(chromedriver)

    def getSoup(self,url):
        self.__browser.get(url)
        for i in range(0,28000,800):   #采用for循环模拟鼠标滚轮下拉，并设置一定时间让图片缓存出来
            js = "window.scrollTo(0,"+str(i)+")"
            self.__browser.execute_script(js)
            time.sleep(0.25)
        soup = BeautifulSoup(self.__browser.page_source)
        self.__browser.quit()
        return soup

    #获取图片链接列表
    def getFileList(self,soup,tag,**kw):
        return [img["src"]  for img in soup.find_all(tag,**kw) ]


    #保存图片
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




if __name__ == "__main__":
    chromedriver = r"./dependence/chromedriver" #selenium的驱动所在
    CONSTURL = "http://ac.qq.com/ComicView/index/id/505430/cid/" #url前面不变的部分
    startIndex = 820 #开始的章节
    endIndex = 843  #结束的章节
    offset = 17 #章节和真正url序号之间的差值
    for index in range(startIndex,endIndex):  #开始每一章节的爬虫
        mybrowser = ChromeBrowser(chromedriver) #生成一个Chrome浏览器
        dir = "./ImgData/" + str(index) + "/" #保存的目录
        link = CONSTURL + str(index + offset) #组合url
        page = mybrowser.getSoup(link) #获取最后经过js渲染之后的真正的页面内容
        imgs = mybrowser.getFileList(page,"img",**{"class":"loaded"}) #获取每一页的图片
        index = 0
        for img in imgs:
            imgName = str(index) + ".jpg"
            mybrowser.saveImage(img, dir, imgName)
            index += 1

    print("已经下载完成")

