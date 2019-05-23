# -*- coding: utf-8 -*-

 

import os
import re
from concurrent import futures
from multiprocessing import cpu_count
from urllib.parse import urlparse
import http.cookiejar as cookielib
import pafy
import lxml
import js2py
import requests
from bs4 import BeautifulSoup

class Core:

    def log(self, message):
        print(message)

    def __init__(self, log_print=None):
        if log_print:
            global print
            print = log_print
        max_workers = cpu_count()*4
        self.executor = futures.ThreadPoolExecutor(max_workers)
        self.executor_video = futures.ThreadPoolExecutor(1)
        self.root_path = "~/Downloads/"
        self.futures = []
        self.session = requests.session()
        self.session.cookies = cookielib.LWPCookieJar(filename=self.root_path+"/_cookie.txt")
        self.defaultHeader = {
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            'dnt': "1",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6",
            'cache-control': "no-cache"}
        self.ajaxheaders = {
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        'dnt': "1",
        'accept-encoding': "gzip, deflate, br",
        'x-requested-with': "XMLHttpRequest",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6",
        'cache-control': "no-cache",
        'accept': "application/json, text/plain, */*; q=0.01",}
        self.headers = {
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
        'dnt': "1",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
        }
 

    def download_by_usernames(self, usernames, type):
        self.no_image = type == 'torrent'
        self.no_video = type == 'image'
        # 去重与处理网址
        # username_set = set()
        # for username in usernames:
        #     username = username.strip().split('/')[-1]
        #     if username not in username_set:
        #         username_set.add(username)
        #         self.download_by_username(username)
        # futures.wait(self.futures)
        # self.log("\n========ALL DONE========")
        startpage=int(usernames[0])
        endpage=int(usernames[1])
        limit=int(usernames[2])
        downloadnum=0
        print("strat:"+str(startpage)+"   endpage:"+str(endpage)+"  limit:"+str(limit))
        for i in range(1,1000):
            if downloadnum > limit and limit !=0:
                print("download finish")
                return
            if i < startpage:
                print("pass:"+str(i))
                continue
            url="http://sex8.cc/forum-798-"+str(i)+".html"
            pagerep=self.getWithHeaderWithCookiesToDirectory(url,self.root_path,self.headers)
            if pagerep==None:
                print("None:"+url)
                err_file=open(self.root_path+"/errs.txt","a")
                err_file.write("page:"+i+ "  "+url+"\n")
                err_file.flush()
                err_file.close()
                continue
            pagetext=pagerep.text
            if pagetext==None:
                print("pagetextNone:"+url)
                err_file=open(self.root_path+'/'+"errs.txt","a")
                err_file.write("page:"+str(i)+" url:"+url+"\n")
                err_file.flush()
                err_file.close()
                continue
            soup = BeautifulSoup(pagetext, 'lxml')
            # print(pagetext)
            datas=soup.find_all('a',onclick='atarget(this)', ) #id=True
            num=0  
            for th in datas:
                if downloadnum > limit and limit !=0:
                    return
                num+=1
                print("..........................")
                url2="http://sex8.cc/"+th['href']
                # url2="http://sex8.cc/thread-12427995-1-1.html"
                print(th.get_text().strip()+"       "+url2)
                page2rep=self.getWithHeaderWithCookiesToDirectory(url2,self.root_path,self.headers )
                if page2rep==None:
                    err_file=open(self.root_path+'/'+"errs.txt","a")
                    err_file.write("page:"+str(i)+"  index:"+str(num)+"  url:"+url2+"\n")
                    err_file.flush()
                    err_file.close()
                    continue
                page2text=page2rep.text
                if page2text==None:
                    err_file=open(self.root_path+'/'+"errs.txt","a")
                    err_file.write("page:"+str(i)+"  index:"+str(num)+"  url:"+url2+"\n")
                    err_file.flush()
                    err_file.close()
                    continue
                soup2 = BeautifulSoup(page2text, 'lxml')
                datas2=soup2.find('td',class_='t_f', id=True) #id=True
                # print(datas2)
                if "影片名称" in str(datas2):
                    if "【影片名称】：" in str(datas2):
                        name=str(datas2).split("【影片名称】：")[1].split('<br')[0]
                    else:
                        name=str(datas2).split("影片名称")[1].split('<br')[0].replace(':','').replace('：','').replace(']','').replace('】','').replace('.','')
                    filenamestr=re.sub(r'[\/:*?"<>|]','-',name.strip().replace('.',''))
                    dirname=self.root_path+'/'+filenamestr+'/'
                    title=soup2.find(id='thread_subject') #id=True
                    if title.contents:
                        dirname=self.root_path+'/'+re.sub(r'[\/:*?"<>|]','-',str(title.contents[0]).strip().replace('.',''))+'/'
                    atags=soup2.find_all('a',target="_blank")
                    imgs=datas2.find_all('img',id=True)

                    downloadimg=False
                    downloadtor=False
                    for atag in atags:
                        if self.no_video :
                            continue
            
                        if atag==None or str(atag)==None:
                            continue
                        if  "href" not in atag.attrs.keys() :
                            continue
                        if  "forum.php?mod=attachment" not in  str(atag.attrs['href']):
                            continue
                        if "." not in str(atag.string):
                            continue
                        download_link="http://sex8.cc/"+atag.attrs['href'] 
                        self.checkFlooder(dirname)
                        if os.path.exists(dirname+str(atag.string).strip()):
                            downloadtor=True
                            continue
                        downloadstate=self.downloadfile(download_link,dirname,(str(atag.string).strip()))
                        # print("download_link====="+download_link)
                        if downloadstate:
                            downloadtor=True
                            downloadnum+=1
                        # else:
                        #     err_file=open(self.root_path+"errs.txt","a")
                        #     err_file.write("page:"+str(i)+"  index:"+str(num)+"  tor not downloaded url:"+url2+"\n")
                        #     err_file.flush()
                        #     err_file.close()
                    for img in imgs:
                        if self.no_image :
                            continue
                        download_link=""
                        if img==None or str(img)==None:
                            continue
                        if  "src" not in img.attrs.keys():
                            if "file" not in img.attrs.keys():
                                continue
                            else:
                                download_link=str(img.attrs['file'])
                        else:
                            download_link=str(img.attrs['src'])
                        if len(download_link)<10 or download_link.endswith('/'):
                            continue
                        if  "http" not in  str(download_link):
                            download_link="http://sex8.cc/"+download_link
                        self.checkFlooder(dirname)
                        if os.path.exists(dirname+(str(download_link.split('/')[len(download_link.split('/'))-1]).strip())):
                            downloadimg=True
                            continue
                        downloadstate=self.downloadfile(download_link,dirname,(str(download_link.split('/')[len(download_link.split('/'))-1]).strip()))
                        if downloadstate:
                            downloadimg=True
                            downloadnum+=1
                        # else:
                        #     err_file=open(self.root_path+"errs.txt","a")
                        #     err_file.write("page:"+str(i)+"  index:"+str(num)+"  img not downloaded url:"+url2+"\n")
                        #     err_file.flush()
                        #     err_file.close()
                        # print("download_link====="+download_link)
                    err_file=open(self.root_path+"/errs.txt","a")
                    if downloadimg ==False:
                        err_file.write("page:"+str(i)+"  index:"+str(num)+"  img not downloaded url:"+url2+"\n")
                        err_file.flush()
                        print("page:"+str(i)+"  index:"+str(num)+"  img not downloaded "+url2)
                    if downloadtor==False:
                        err_file.write("page:"+str(i)+"  index:"+str(num)+"  tor not downloaded "+url2+"\n")
                        err_file.flush()
                        print("page:"+str(i)+"  index:"+str(num)+"  tor not downloaded "+url2)
                    err_file.close()
                    print("now:page"+str(i)+" index:"+str(num) +" url: "+url +" indexurl:"+url2)
                    print("**************************")
                else:
                    print("page:"+str(i)+"  index:"+str(num)+" url: "+url +" not downloaded "+url2)
                    print("now: page"+str(i)+"  index:"+str(num) )
                    print("**************************")
    
    def getWithHeaderWithCookiesToDirectory(self,url,directory,header):
        # print("directory:"+directory)
        sessionfile_full_path = os.path.join(directory, self.getURI(url)+"_cookie.txt")
        if os.path.exists(sessionfile_full_path):
            pass
            # print('[Exist][cookie][{}]'.format(sessionfile_full_path))
        else:
            # print("creat Cookie File:"+sessionfile_full_path)
            os.makedirs(directory, exist_ok=True)
        self.session.cookies = cookielib.LWPCookieJar(filename=sessionfile_full_path)
        # print("Open:"+url)
        try:
            responseRes=self.session.get(url,  headers = header ) 
            # print(responseRes)
            return responseRes
        except Exception as e:
            print(e)
            return None
        finally:
            self.session.cookies.save()
        if not responseRes.ok:
            print("ERR CODE:"+str(responseRes.status_code))
            return self.getWithHeaderWithCookiesToDirectory(url,directory,header) 
        return responseRes

    def getURI(self,url):
        if "http" not in url:
            if "." not in url:
                return ""
            else:
                if "/" not in url:
                    return url
                else:
                    strs=url.split('/')
                    return strs[0]
        else:
            strs=url.split('://')
            return strs[1].split('/')[0]
        return ""
    
    def checkFlooder(self, directory):
        # print("checking {} ...".format(str(directory).split()))
        if os.path.exists(str(directory)):
            return
            # print('[Exist][directory][{}]'.format(str(directory)))
        else:
            # print("creat directory :"+str(directory))
            os.makedirs(str(directory), exist_ok=True)
    
    def downloadfile(self,url,directory,filename):
        print("downloading URL:"+url+" as filename: "+filename +" into "+directory)
        _filename = (directory+'/'+re.sub(r'[\/:*?"<>|]','-',filename)).replace('//','/')
        try:
            response = requests.get(url, headers=self.defaultHeader)
            with open(_filename.encode('UTF-8').decode("UTF-8"), 'wb') as f:
                f.write(response.content)
                f.flush()
                f.close()
                return 1
        except Exception as e:
            print(e)
            return 0
        finally:
            f.close()
        return 0
