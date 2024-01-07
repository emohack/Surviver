from json import loads

class Filter:
    def __init__(self):
        # 读取filter.json文件，获取过滤规则
        with open("configs/Filter.json","r") as f:
            data=f.read()
        filter=loads(data)
        self.Host=filter["Host"]
        self.Title=filter["Title"]
        self.Status=filter["Status"]
        self.Length=filter["Length"]



    def run(self,rsp):
        # 检查Host
        if self.Host != "":
            if self.filter(rsp.url.split("//")[1].split("/")[0],self.Host):
                return False
        # 检查Title
        if self.Title != "":
            if self.filter(rsp.text.split("<title>")[1].split("</title>")[0],self.Title):
                return False
        # 检查Status
        if self.Status !="":
            if self.filter(rsp.status_code,self.Status):
                return False
        # 检查Length
        if self.Length !="":
            if self.filter(len(rsp.text),self.Length):
                return False
        return True

    def filter(self,data,filter):
        # 以,分割
        filters=filter.split(",")
        for f in filters:
            if str(f)==str(data):
                return True
        return False