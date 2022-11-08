from cmd_cur import *
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

    def mainloop(self, timeout:Union[int,float]=-1, doUpDown:bool=True) -> bool:
        '''
        开始一轮事件循环，监听键盘事件
        参数
        ===========================
        timeout: 超时的秒数（无：-1）
        doUpDown: 监听方向键
        ===========================
        返回值：是否超时
        '''
        endt = time.time() + timeout
        while True:
            ch = getwch()
            if ch == 'H' and doUpDown:
                self.select(self.i - 1)
            if ch == 'P' and doUpDown:
                self.select(self.i + 1)
            elif ch in '\r\n':
                return False
            if timeout != -1 and time.time() >= endt:
                return True
                

    def next(self, p:str, options:List[str], timeout:Union[int,float]=-1) -> int:
        '''
        新增一段故事，并要求玩家做出选择
        参数
        ==============
        p: 故事新增文段
        options: 选项
        timeout: 超时的秒数（无：-1）
        ==============
        返回值
        ====
        未超时，返回选择的序号；
        超时，返回-1
        ====
        '''
        # 更新变量
        self.n = len(options)  
        self.i = 0
        self.options = options
        # 更新故事文段
        self.paragraph += p + '\n'  
        print(p)

        _, rl = getxy()  # 记住光标位置，方便回退

        # options 为空处理
        if not options:
            self.mainloop(timeout, doUpDown=False)
            return -1

        # 绘制选项
        self.flush(delline=False, showopt=True)
        # 事件循环
        flag = self.mainloop(timeout)

        self.flush(cover=True)  # 清除选项
        gotoxy(0, rl)  # 回退光标

        if flag:
            return -1
        else:
            return self.i

    def flush(self, delline:bool=True, showopt:bool=False, cover:bool=False):
        '''
        刷新选项
        参数
        ====================
        delln: 是否覆盖原来的选项
        showopt: 是否刷新选项名称
        cover: 是否删除原来的选项
        ====================
        '''
        if delline:
            delln(self.n)
        for i in range(self.n):
            if cover:
                print(' ' * (4+len(self.options[i])*2))  # *2是因为有全宽字符，+4是因为选择框('[ ] ')
            else:
                print('[*]' if (self.i==i) else '[ ]',  # 是否被选择
                      self.options[i] if showopt else '')
            
    def select(self, i:int, flush:bool=True):
        self.i = i % self.n
        if flush:
            self.flush()

            
if __name__ == '__main__':
    cgm = CGMain()
    op = ['好啊，很好啊', '不好不好']
    c = cgm.next('你好, CGE', op)
    if c == -1:
        print('timeout')
    else:
        print(op[c])
    print('按任意键退出...')
    getwch()