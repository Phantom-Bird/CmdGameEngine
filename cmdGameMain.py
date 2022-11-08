from cmd_cur import delln
import time
from typing import List, Union
from msvcrt import getwch

SELECT = '*'

def show(*args):
    '''
    print(*args, sep='', end='', flush=True)
    '''
    print(*args, sep='', end='', flush=True)

class CGMain():
    def __init__(self):
        self.paragraph:str = ''  # 故事
        self.options:List[str] = []  # 选项
        self.n:int = 0  # 选项个数
        self.i:int = 0  # 当前选项

    def mainloop(self, timeout:Union[int,float]=-1, doUpDown:bool=True):
        pass

    def next(self, p:str, options:List[str], timeout:Union[int,float]=-1):
        '''
        新增一段故事，并要求玩家做出选择
        参数
        ==============
        p: 故事新增文段
        options: 选项
        timeout: 超时的秒数（无默认为-1）
        ==============
        返回值
        ====
        未超时，返回选择的序号；
        超时，返回None
        ====
        '''
        # 更新变量
        self.n = len(options)  
        self.i = 0
        self.options = options
        # 更新故事文段
        self.paragraph += p + '\n'  
        print(p)

        # options 为空处理
        if not options:
            self.mainloop(timeout, doUpDown=False)
            return None

        self.flush(delline=False)
        self.mainloop(timeout)
        self.flush(showopt=False)

    def flush(self, delline:bool=True, showopt:bool=True):
        '''
        刷新选项
        参数
        ====================
        delln: 是否删除原来的选项
        showopt: 是否显示新选项
        ====================
        '''
        if delline:
            delln(self.n)
        if showopt:
            for i in range(self.n):
                print('[*]' if (self.i==i) else '[ ]', self.options[i])
                #              是否被选择
            
if __name__ == '__main__':
    cgm = CGMain()

    # 流水选项
    cgm.next('Hello', list('ABCDE'))
    cgm.flush(False)  # 为了对抗清屏，请勿模仿
    for _ in range(2):
        for i in range(5):
            cgm.i = i
            cgm.flush()
            time.sleep(0.2)