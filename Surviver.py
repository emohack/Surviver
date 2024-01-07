import argparse,requests
import multiprocessing
import time

import fake_useragent

from configs.Out import Out
from configs.Filter import Filter
from configs.ProcessFile import *
from configs.Config import *

# 忽略https证书验证
requests.packages.urllib3.disable_warnings()

class Surviver(object):
    def __init__(self, file,proxy=None):

        self.o=Out(file)
        self.filter=Filter()

        self.file=file

        self.headers={
            "User-Agent":fake_useragent.UserAgent().random,
            "Accept-Encoding":"gzip, deflate",
            "Accept":"*/*",
            "Connection":"close"
        }
        self.proxies=None
        if proxy:
            if proxy.startswith("http://"):
                self.proxies={
                    "http":proxy
                }
            elif proxy.startswith("https://"):
                self.proxies={
                    "https":proxy
                }
            elif proxy.startswith("socks4://"):
                self.proxies={
                    "socks4":proxy
                }
            elif proxy.startswith("socks5://"):
                self.proxies={
                    "socks5":proxy
                }
            else:
                cprint("[-] Proxy Error!", "red")
                exit(0)

    def verify(self,url):
        url=url
        try:
            rsp=requests.get(url,verify=False,timeout=3,allow_redirects=True,headers=self.headers,proxies=self.proxies)
            if not self.filter.run(rsp):
                return
            # rsp = requests.post(url, verify=False, timeout=5, allow_redirects=False, headers=self.headers,proxies=self.proxies,data=self.data)
            self.Cout(rsp)

        except Exception as e:
            # cprint("[-] Error: "+str(e), "red")
            # self.Cout(e)
            pass



    def run(self,url):
        url = url
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.verify(url)


    def Cout(self,rsp):
        self.o.Out(rsp)

    #
    def WirteFile(self):
        self.o.WriteFile()

def thread_work(file,options,poc):
    with open(file) as ff:
        with ThreadPoolExecutor(options.thread) as executor:
            for line in ff:
                executor.submit(poc.run, line.strip())
    poc.WirteFile()


if __name__ == '__main__':
    banner()
    args=argparse.ArgumentParser()
    args.add_argument('-f', '--file', help='Target File')
    args.add_argument('-t', '--thread', help='Number of Thread,default is 10', default=20)
    args.add_argument('-p', '--proxy', help='Proxy (http/https/socks4/socks5)://127.0.0.1:1234)', default=None)
    args.add_argument('-d','--directory',help="the target files' directory",default=None)

    options = args.parse_args()

    if not options.file and not options.directory:
        cprint("Please Input the target file!", "red")
        args.print_help()
        exit()

    if options.file and options.directory:
        cprint("Please Input the target file or directory!", "red")
        args.print_help()
        exit()


    # 是否存在output文件夹
    if not os.path.exists("output"):
        os.mkdir("output")
    # 创建下级目录
    outdir="output/"+options.file.split("/")[-1].split(".")[0]+"_"+time.strftime("%H%M%S", time.localtime())
    os.mkdir(outdir)

    files = options.file if options.file else options.directory
    p = ProcessFile(files)
    file = p.run(outdir)

    output=outdir+"/output.csv"
    f=open(output,"w")
    poc=Surviver(f,options.proxy)
    thread_work(file,options,poc)

    # 关闭文件
    f.close()
    print()
    print("[+] Output file: "+output)
