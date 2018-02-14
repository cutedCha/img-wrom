import requests
import re
import os
from bs4 import BeautifulSoup
class test_get() :
    def start(self) :
        n = 0
        while n <= self.max_n :
            try :
                req = requests.get(self.u,headers=self.headers,data=self.data,timeout=self.timeout)
            except Exception :
                print('请求时发生蜜汁的错误重新尝试已尝试%d次' % (n))
                req = False
            else :
                break
            n+=1
        if req == False :
            return
        self.text = req.text
        self.req = req
        self.req.encoding = self.encoding
        self.text = req.text
    def __init__(self,u,max_n=10,data={},timeout=20,encoding='utf-8'):#最大尝试次数
        self.encoding = encoding
        self.data = data
        self.timeout = timeout
        self.max_n = max_n
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
        self.u = u
    def __str__(self) :
        return str(self.text)
#hh = test_get('https://www.w3cschool.cn/') #例子必须给定一个url可选参数为最大请求次数其他参数随意
#hh.start() #定义好后不会立马请求然后调用start()方法才能启动在此之前你可以修改headers
#print(hh)#req为请求的requests对象下载文件用content打印网页为text亦可start完之后直接打印网页默认的__str__就是网页内容
class get_url_bottom() :
    def __init__(self,u) :
        b = re.findall('(?<=\/)[^\/]{1,}',u)
        self.bottom = b.pop()
        self.bottom = re.sub('\?','_',self.bottom)
    def __str__(self) :
        return self.bottom
#hh = get_url_bottom('https://wadadwwdasdafaadaffasb.ssdac/adaf.sdaf/ssfadadh')
#print(hh)这个类用于提取文件的名字用法直接给一个url就会自动匹配了
class dw_file() :#下载一些图片的类
    def dw(self) :
        n = 0
        while 10 >= n :
            try :
                req = requests.get(self.u)
            except Exception :
                req = False
                print('蜜汁错误重新尝试')
            else :
                break
                pass
            n+=1
        if req != None :
            print('req存在')
            f_path = self.dir +'%s' % (self.name)
            if os.path.exists(self.dir) == False :
                try :
                    os.makedirs(self.dir)
                except Exception :
                    print('创建文件夹时发生蜜汁的错误')
                    return
                else :
                    pass
            with open(f_path,'wb+') as f :
                f.write(req.content)
    def __init__(self,u,dir = None,name = None) :
        self.u = u
        if dir == None :
            self.dir = './'
        else :
            self.dir = dir
        if name == None :
            self.name = get_url_bottom(self.u)
        else :
            self.name = name
#dw = dw_file('https://www.baidu.com/img/bd_logo1.png',dir = './ssd/')
#dw.dw()#用法一个必须的参数下载文件的url可选参数文件的名字name和文件存储的dir
#定义完不会立即下载要用dw()方法这样写方便在下载之前修改
class test_tag() :#尝试一个html元素存在不存在的类
    def __init__(self,bs4_obj,tag) :
        self.bs4_obj = bs4_obj
        self.tag = self.bs4_obj.select(tag)
        if len(self.tag) > 0 :
            self.bool = True
        else :
            self.bool = False
    def __repr__(self) :
        if self.bool == True :
            return 'True'
        else :
            return "False"
#req = test_get('http://96xxnet.com',encoding='gbk')
#req.start()
#html = req
#html = str(html)
#bs4_obj = BeautifulSoup(html, "html.parser")
#hh = test_tag(bs4_obj,'.next_page')
#if hh.bool == True :
#    print('这个元素存在')
#else :
#    print('不存在')
#print(hh.tag)
