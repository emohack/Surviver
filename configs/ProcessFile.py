# 读取传入的文件，对文件内容进行去重、排序
# 生成新的文件，文件名为：原文件名_去重_排序.txt

import os
from concurrent.futures import ThreadPoolExecutor


class ProcessFile(object):
    # 对传入文件参数个数不做限制
    def __init__(self, files):
        self.file = []
        self.data = []
        self._number=0

        self._del_file(files)


    def _process(self,file):
        with open(file,'r') as f:
            for line in f:
                if line not in self.data:
                    self.data.append(line)

    def run(self,outdir):
        # 多线程处理
        with ThreadPoolExecutor(self._number) as executor:
            executor.map(self._process,self.file)
        return self._end(outdir)

    def _end(self,outdir):
        # data去重
        self.data=list(set(self.data))
        self.data=sorted(self.data)

        # 生成新文件
        newfile=outdir+"/sorted.txt"
        with open(newfile,'w') as f:
            for line in self.data:
                f.write(line)
        return newfile

    def _del_file(self,files):
        # 检查传入参数是文件还是文件夹
        if os.path.isfile(files):
            self.file.append(files)
            self._number=1
        elif os.path.isdir(files):
            for file in os.listdir(files):
                self.file.append(files+"/"+file)
                self._number+=1
        else:
            print("Please input the right file or directory!")
            exit()

        if self._number>5:
            self._number=5

        elif self._number==0:
            print("There is no file in the directory!")
            exit()

