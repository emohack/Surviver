import re

from termcolor import cprint
from configs.Config import *
from configs.Lock import *


class Out:
    def __init__(self, file):
        self.f = file
        # 写入表头
        self.f.write("Host,URL,Title,Status,Length\n")
        self.f.flush()
        self.datas=[]
        
    def Out(self,rsp):
        if rsp.status_code==200:
            color="green"
        elif rsp.status_code==403:
            color="yellow"
        elif rsp.status_code==404:
            color="red"
        else:
            color="cyan"

        # 输出网页url + 标题 + 状态码
        cprint("URL: " + rsp.url, color,end=" , ")
        try:
            title=re.findall(r'<title>(.*?)</title>', rsp.text, re.I)[0]
        except:
            title=" "
        cprint("Title: " + title, color,end=" , ")
        cprint("Status: " + str(rsp.status_code), color,end=" , ")
        # 输出网页长度
        cprint("Length: " + str(len(rsp.text)), color)
        host = rsp.url.split("//")[1].split("/")[0]

        data=Detection(host,rsp.url,str(rsp.status_code),title,str(len(rsp.text)))
        self.datas.append(data)

        
    def WriteFile(self):
        for data in self.datas:
            # 写入文件
                self.f.write(
                    data.host + "," + data.url + "," + data.title + "," + data.status + "," + data.length + "\n")
                self.f.flush()