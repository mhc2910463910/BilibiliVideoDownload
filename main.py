import sys
import webbrowser
import threading
from functools import partial
from tkinter import END
import requests
import bs4
from selenium.common import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import tkinter
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import time
import requests
import re
import bs4
import os
import webbrowser
# import ffmpeg
import pyperclip
class bilibili:
    def __init__(self,mytext):
        print("开始")
        self.mytext=mytext
        # 搜索内容
        self.res={}
        # 存储搜索结果
    def start(self):
        opt = Options()
        opt.add_argument('--headless')
        opt.add_argument('disbale-gpu')  # 无头模式
        opt.add_argument("user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")
        # opt.binary_location="/opt/apps/cn.google.chrome/files/google/chrome/chrome"
        service=Service('/opt/apps/cn.google.chrome/files/google/chrome/chromedriver')
        # self.web=Chrome(service =service,options=opt) #无头模式
        self.web=Chrome(service =service)
        # 调用谷歌浏览器
        self.web.get(f"https://search.bilibili.com/video?keyword={self.mytext}")
        # # 打开主页
        # self.web.find_element(By.XPATH,'//*[@id="nav-searchform"]/div[1]/input').send_keys(self.mytext,Keys.ENTER)
        # # 定位搜索框
        # time.sleep(2)
        # # 延时，等待加载网页
        # self.web.switch_to.window(self.web.window_handles[-1])
        # # 切换窗口到搜索结果页面
        return
    def getUrl(self,i):
            # 获取第i个搜索结果
            self.res={}
            try:
                try:
                    page_author = self.web.find_element(By.XPATH,f'//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div[1]/div[{i}]/div/div[2]/div/div/div/a/span[1]')
                    page_name = self.web.find_element(By.XPATH,f'//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div[1]/div[{i}]/div/div[2]/div/div/a/h3').text
                    page_url = self.web.find_element(By.XPATH,f'//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div[1]/div[{i}]/div/div[2]/div/div/a')
                    # 搜索结果第一页html代码解析
                except Exception as e:
                        print(f"{e}")
                self.res = {
                        "简介": page_name.text,
                        "作者": page_author.text,
                        "地址": page_url.get_attribute('href'),
                    }
                # 搜索内容存储在字典中
                print(f"第{i}个结果:")
                print(page.text + " " + page_name)
                print(page_url.get_attribute('href'))
            except Exception as e:
                print(f"获取失败{e}")
            finally:
                sys.stdout.flush()
                    # 强制刷新缓存区,打印结果
                time.sleep(1)
    def getPage(self,i):
        # 翻页
        self.web.get(f"https://search.bilibili.com/all?keyword={self.mytext}&from_source=webtop_search&spm_id_from=333.1007&search_source=5&page={i}&o={30 * i}")
class Tkbilibili:
    # tk界面
    def __init__(self,title):
        self.root = tkinter.Tk()
        self.root.title=title
        self.root.maxsize(300,400)
        self.root.minsize(200,200)
        self.thread1 = threading.Thread(group=None, target=self.start, args=(), daemon=None)
        # 线程一，加载界面
        self.thread2 = threading.Thread(group=None, target=self.search, args=(), daemon=None)
        # 线程二，后台爬取数据
        self.num=1
        self.page_res=1
        # 页码
        self.bili=[]
    def Entry(self):
        self.entry=tkinter.Entry(
            self.root,
            show="",
            width=100,
            font=('Helvetica', '20', 'bold'),
            bg='black',
            fg='white',
        )
        # tk文本框，输入搜索内容
        self.entry.insert(END,"")
        self.entry.pack(side='top')
    def button(self):
        self.start_but=tkinter.Button(
            self.root,
            text="搜索",
            width=15,
            height=2,
            bg="black",
            foreground="white",
            command=self.thread_start
        #     按钮事件，开始线程一
        )
        # 搜索按钮
        self.start_but.pack(side='top',fill='x')
        self.close_but=tkinter.Button(
            self.root,
            text = "关闭",
            width = 15,
            height = 2,
            bg = "black",
            foreground = "white",
            command=self.exits
        )
        # 关闭按钮
        self.close_but.pack(side='top',fill='x')
        self.up_but = tkinter.Button(
            self.root,
            text="上一页",
            width=15,
            height=2,
            bg="black",
            foreground="white",
            command=self.up_page
        )
        # 上一页
        self.up_but.pack(side='top', fill='x')
        self.down_but = tkinter.Button(
            self.root,
            text="下一页",
            width=15,
            height=2,
            bg="black",
            foreground="white",
            command=self.down_page
        )
        # 下一页
        self.down_but.pack(side='top', fill='x')
    def exits(self):
        self.bili.web.quit()
        # 关闭浏览器
        sys.exit()
    #     退出程序
    def text(self):
        self.entrys=tkinter.Text(
            self.root,
            font=('仿宋', '10', 'bold'),
            bg="white",
            width=200,
            height=100,
            foreground = "black",
        )
        # 工具文本框显示程序运行数据
        self.entrys.insert(END,"bilibili下载工具")
        self.entrys.pack(side='bottom',fill='x',expand=True)
    def thread_start(self):
        self.thread1.start()
    #     开启线程一
    def start(self):
        self.bili = bilibili(self.entry.get())
        self.bili.start()
        time.sleep(7)
        self.thread2.start()
    #     打开浏览器，等待页面加载完成，开启线程二，搜索内容
    def search(self):
        colum=1
        self.entrys.insert(END, "\n正在查询,请耐心等待...\n")
        # 文本框提示信息
        self.inf = info()
        # 创建窗口2,显示搜索结果
        time.sleep(2)
        for i in range(1,31):
            # b站网页版全屏模式，一页显示30个内容，因此此处搜索为一页内容
            self.thread2=threading.Thread(group=None, target=self.bili.getUrl, args=(i,), daemon=None)
            self.thread2.start()
            # 线程2开始搜索数据
            time.sleep(3)
            # 此处可更改延时时间
            print(self.bili.res)
            try:
                resu = self.bili.res
                # 搜索结果，字典格式
                self.inf.label(resu,colum)
                # 将字典信息输出到窗口2
                self.write(resu)
            #     搜索结果写入到文本框
            except Exception:
                self.inf.label({'简介':'获取失败','地址':'https://www.bilibili.com/'},colum)
                self.write({'简介':'获取失败','地址':'https://www.bilibili.com/'})
            #     异常捕获
            colum+=1
            if colum>=3:
                colum=1
            #     窗口2的列数，2列时换行
            # print(colum)
        # self.inf.pages()
        self.inf.display()
        # 搜索完成，窗口2显示
        self.win()
    #     文本框提示搜索完成
    def write(self,infos):
        self.entrys.insert(END,"\n"+f"{self.num}个结果"+infos['简介'])
        # 文本提示框写入信息
        self.num+=1
    def up_page(self):
        # 上翻页
        self.page_res-=1
        self.bili.getPage(self.page_res)
        # 向上翻页
        time.sleep(1)
        self.thread2=threading.Thread(group=None, target=self.search, args=(), daemon=None)
        self.thread2.start()
    #     线程二开始搜索
    def down_page(self):
        # 下翻页
        self.page_res+=1
        self.bili.getPage(self.page_res)
        # 网页向下翻页
        time.sleep(1)
        self.thread2 = threading.Thread(group=None, target=self.search, args=(), daemon=None)
        self.thread2.start()
    #     线程二开始搜索
    def win(self):
        self.entrys.insert(END, "\n查询完成\n")
        # 搜索完成
        self.bili.web.close()
    #     关闭浏览器
    def display(self):
        # 窗口显示在电脑屏幕
        self.Entry()
        self.button()
        self.text()
        self.root.mainloop()

class info(Tkbilibili):
    # 窗口2,显示搜索结果
    def __init__(self):
        self.root=tkinter.Tk()
        self.row=int(1)
    #     行数
    def label(self, results,flag):
        # print(f"flag={flag}")
        # label标签，显示搜索内容
        if flag==1:
            # flag==1,第一列显示
            label = tkinter.Label(
                self.root,
                bg="white",
                fg="black",
                text=results['简介'],
                font=('仿宋', '10'),
                width=60,
                height=1,
                anchor="nw",
            )
            label.grid(
                # column=1,
                columnspan=5,
                row=self.row
            )
            # Button标签，打开浏览器
            but=tkinter.Button(
                self.root,
                bg='black',
                fg='white',
                text='打开',
                width=7,
                height=1,
                command=partial(self.open, results['地址']),
            )
            but.grid(
                column=5,
                row=self.row
            )
            # Button标签，下载视频，暂未添加实际功能
            down=tkinter.Button(
                self.root,
                bg='black',
                fg='white',
                text='下载',
                width=7,
                height=1,
                command=partial(self.down, results['地址']),
            )
            down.grid(
                column=6,
                row=self.row
            )
        else:
            # 第二列显示
            label = tkinter.Label(
                self.root,
                bg="white",
                fg="black",
                text=results['简介'],
                font=('仿宋', '10'),
                width=70,
                height=1,
                anchor="nw",
            )
            label.grid(
                column=7,
                columnspan=5,
                row=self.row
            )
            but = tkinter.Button(
                self.root,
                bg='black',
                fg='white',
                text='打开',
                width=7,
                height=1,
                command=partial(self.open, results['地址']),
            )
            but.grid(
                column=12,
                row=self.row
            )
            down = tkinter.Button(
                self.root,
                bg='black',
                fg='white',
                text='下载',
                width=7,
                height=1,
                command=partial(self.down, results['地址']),
            )
            down.grid(
                column=13,
                row=self.row
            )
        if flag>=2:
            self.row+=1
    def open(self,url):
        # 浏览器打开指定视频
        print(url)
        webbrowser.open(url)
    def down(self,url):
        # res=requests.get(url)
        # print(res.text)
        print(url)
        DownLoad(url)
    def display(self):
        self.root.mainloop()
#         窗口二显示

def DownLoad(url):
    print("""bilibili视频下载程序""")
    # print("请输入视频地址:")
    urllink=url
    # urllink=pyperclip.paste()
    url=urllink
    res=requests.get(url)
    # print(res.text)
    text=bs4.BeautifulSoup(res.text,'html.parser')
    text_name=text.find('title').text
    print(text_name)
    if " " in text_name:
        text_name=text_name.replace(" ","-")
    # print(text_name)
    obj=re.compile('"codecid":7},{"id":32,"baseUrl":"(?P<info>.*?)","base_url":".*?',re.S)
    page=obj.finditer(res.text)
    for li in page:
        vudiourl=li.group("info")
                # print(li.group("info"))
        musobj=re.compile('{"id":30280,"baseUrl":"(?P<mus>.*?)","base_url":.*?')
        muspage=musobj.finditer(res.text)
        for li in muspage:
            audiourl=li.group("mus")
                # print(audiourl)
        head={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
            "Referer":url,
            }
        vudiores=requests.get(vudiourl,headers=head)
        audiores=requests.get(audiourl,headers=head)
            # print(vudiores)
            # print(audiores)
        vudio=vudiores.content
        music=audiores.content
        try:
            os.makedirs(f"{text_name}")
        except:
            pass
        with open(f"{text_name}//vudio.mp4",'wb') as fie:
            fie.write(vudio)
        with open(f"{text_name}//audio.mp4",'wb') as fie:
            fie.write(music)
        # print(os.listdir(f"{text_name}"))
        file1=f"{text_name}//vudio.mp4"
        file2=f"{text_name}//audio.mp4"
        result=f"{text_name}//output.mp4"
        print("下载中...")
        os.system(f"ffmpeg.exe -i {file1} -i {file2} -c:v copy -c:a copy {result}")
        time.sleep(5)
        print("下载完成...")
try:
    bili=Tkbilibili("bilibili视频播放下载器")
    bili.display()
except:
    bili.exits()













