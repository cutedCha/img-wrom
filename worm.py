import requests
from bs4 import BeautifulSoup
import queue
import threading
import sys
import re
from tools.tools import dw_file,test_get
import os
a_list_array = []#1级目录的数组
b_list_array = []#2级数组
B = threading.Event()
c_list_array = queue.Queue()
bool_g = True
class get_lks() :
    def get(self) :
        req   = test_get('https://www.deviantart.com')
        req.start()
        html = BeautifulSoup(req.text, "html.parser")
        lists = html.select('.cat-depth-0')
        print('一阶目录爬行')
        for item in lists :
            lk = item.attrs['href']
            a_list_array.append(lk)
        print('二阶目录爬行中请等待')
        #print('ps导师你脑子有毛病')
        for item in a_list_array :
            #print(item)
            print(item)
            if item != 'https://www.deviantart.com/traditional/whats-hot/' :
                continue
            print(item)
            req = test_get(item)
            req.start()
            html = BeautifulSoup(req.text, "html.parser")
            lists = html.select('.cat-depth-2')
            for item in lists :
                req = test_get(item.attrs['href'])
                req.start()
                #print(req)
                html = BeautifulSoup(req.text, "html.parser")
                #print(item)
                #print(item.attrs['href'])
                b_list_array.append(item.attrs['href'])
                lists = html.select('.cat-depth-3')
                for item in lists :
                    c_list_array.put(item.attrs['href'])
        B.set()
        print('所有的链接都爬行完毕')
        sys.exit()
                #print(b_list_array.get())
        #print('三阶目录爬行')
        #for item in b_list_array :
        #    #print(item)
        #    req = test_get(item)
        #    req.start()
        #    html = BeautifulSoup(req.text, "html.parser")
        #    lists = html.select('.cat-depth-3')
        #    for item in lists :
        #        #print(item)
        #        #print(item.attrs['href'])
        #        c_list_array.put(item.attrs['href'])
                #print(b_list_array.get())
t = threading.Thread(target=get_lks().get,args=())
t.start()

class dw_imgs() :
    def dw_imgs(self) :
        while True :
            if c_list_array.empty() == True and B.is_set() == True :
                print('kill a threading')
                sys.exit()
            try :
                self.lks = c_list_array.get(block=False)
            except Exception :
                #print('获取b到重试')
                continue
            #print(self.lks)
            self.dir_name = re.search('(?<=\.com).+(?=whats-hot)',self.lks).group()
            self.get_imgs()
            #print(self.dir_name)
    def get_imgs(self) :
        n = 0
        while True :
            #print('导师是狗')
            fmt_str = self.lks + '?offset=%d'
            url = fmt_str % (n)
            print(url)
            req = test_get(url)
            req.start()
            if re.search('Sorry, DeviantArt does not serve',req.text) != None :
                break#如果文件不存在就退出循环
            try :
                LE = len(os.listdir('./图片'+self.dir_name))
                print('./图片'+self.dir_name+str(LE)+'有张图片')
                if LE >= 5000 :
                    break
            except Exception :
                pass
            html = BeautifulSoup(req.text,"html.parser")
            img_array = html.select('.torpedo-thumb-link img')
            #print(img_array)
            for item in img_array :
                print('下载'+str(item.attrs['src']))
                dw_file(item.attrs['src'],dir='./图片'+self.dir_name).dw()
            n+=24
            #break
#def d() :
#    dw_imgs().dw_imgs()
N = 0
while N < 300 :
    T = threading.Thread(target=dw_imgs().dw_imgs,args=())
    T.start()
    N+=1
sys.exit()
