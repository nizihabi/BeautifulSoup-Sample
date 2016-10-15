from bs4 import BeautifulSoup
from urllib import request
from collections import OrderedDict
import re
import os

BASE_URL = r"http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000"
START_ID = "0014316089557264a6b348958f449949df42a6d3a2e542c000"

dir = "./data"  #储存爬虫下来的数据的目录，按网站的目录进行分类保存

#保存某个分支目录下的信息
def saveContent(contInfo,filename):
    if not os.path.exists(dir):
        os.makedirs(dir)

    with open(dir+"/"+filename,"w") as f:
        for coni in contInfo:
            for texts in coni.find_all(re.compile(r"p|a|ul|li")):
                if texts != "\n" and texts.string != None:
                    f.write(texts.string)
                    if texts.name == "a":
                        f.write(texts["href"])


#爬虫获取详细信息
def get_wiki_data(wikiid, name):
    wikiurl = ""
    if wikiid == START_ID:
        wikiurl = BASE_URL
    else:
       wikiurl = BASE_URL + r"/" + k
    try:
       # print(wikiurl)

        wikipage = request.Request(wikiurl)
        request.urlcleanup()
        wikipagecontent = request.urlopen(wikipage).read()
    except:
        return

    wikiSoup = BeautifulSoup(wikipagecontent)
    contentInfo = wikiSoup.find_all("div",{"class":"x-wiki-content"})
    name = re.compile(r"\\|#|@|&|/|\?|\*").sub("",name)
    savefile = name + ".txt"
    print(savefile)
    try:
        saveContent(contentInfo,savefile)
    except Exception as e:
        print(e)


if __name__ == "__main__":

    #获取章节目录
    try:
        wikiIndex=OrderedDict()
        page = request.Request(BASE_URL)
        pagecontent = request.urlopen(page).read()
        soup = BeautifulSoup(pagecontent)
        ur  = soup.find_all("ul",{"class":"uk-nav uk-nav-side","style":"margin-right:-15px;"})[0]
        for li in ur.find_all("li"):
            if '\n' in li.contents:
                wikiIndex[li["id"]] = li.contents[1].string
            else:
                wikiIndex[li["id"]] = li.contents[0].string
        #按上面爬到的目录进行遍历获取每个目录的内容
        for k,v in wikiIndex.items():
            get_wiki_data( k,v)

    except:
        pass