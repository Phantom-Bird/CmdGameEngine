from cmd_cur import *
import time
from typing import List, Union
from msvcrt import getch, kbhit
from const import *


def show(*args:str, delete:bool=False):
    '''
    print(*args, sep='', end='', flush=True)
    参数
    ====================================
    delete: 为真时将所有非空字符替换成空格
    ====================================
    '''
    if delete:
        dels(''.join(args))
    else:
        print(*args, sep='', end='', flush=True)

def dels(string:str):
    rows = string.splitlines()
    for i in rows:
        print(' ' * len(i) * 6)  # ascii空格不会在cmd导致换行，随便浪

class CGMain():
    def __init__(self):
        self.paragraph:str = ''  # 故事
        self.options:List[str] = []  # 选项
        self.n:int = 0  # 选项个数
        self.i:int = 0  # 当前选项
        self.sx:int = 0  # 当前故事部分结束位置
        self.sy:int = 0

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
        start = time.time()
        print()  # 进度条另起一行
        _, tby = getxy()  # 记住进度条位置，方便回退

        while True:
           
            t = time.time() - start
            if t >= timeout:
                show('\r', ' '*60)  # 消除痕迹是个好习惯
                return True
            
            # 进度条长度为50
            a = int(t*50//timeout)
            b = 50 - a
            show('\r时限[', BLOCK*a, ' '*b, ']')

            if kbhit():  # 超时判断不能阻塞
                ch = getch()
                if (ch==b'H' or ch==b'K') and doUpDown:  # ↓：'\xe0H'；←：'\xe0K'
                    self.select(self.i - 1)
                elif (ch==b'P' or ch==b'M') and doUpDown:  # ↑：'\xe0P'；→：'\xe0M'
                    self.select(self.i + 1)
                elif ch == b'\r':
                    if timeout == -1:
                        show('\r', ' '*60)  # 消除痕迹是个好习惯
                    return False
                gotoxy(0, tby)

            time.sleep(TICK_SEC)
        
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

        self.sx, self.sy = getxy()  # 记住光标位置，方便回退

        # options 为空处理
        if not options:
            self.mainloop(timeout, doUpDown=False)
            return -1

        # 绘制选项
        self.flush()
        # 事件循环
        flag = self.mainloop(timeout)

        self.flush(cover=True)  # 清除选项
        self.back2story()  # 回退光标

        if flag:
            return -1
        else:
            return self.i

    def flush(self, cover:bool=False):
        '''
        刷新选项
        参数
        ========================
        cover: 是否删除原来的选项
        ========================
        '''
        self.back2story()
        for i in range(self.n):
            show('[*] ' if (self.i==i) else '[ ] ',  # 是否被选择
                 self.options[i],
                 delete=cover)
            
    def select(self, i:int, flush:bool=True):
        self.i = i % self.n
        if flush:
            self.flush()

    def back2story(self):
        gotoxy(self.sx, self.sy)


            
if __name__ == '__main__':
    cgm = CGMain()
    op = ['好好好    ', '不好不好    ', '鬼！']
    c = cgm.next('你好, CGE', op, timeout=10)
    if c == -1:
        print('你在犹豫什么？')
    elif c == 0:
        print('好！')
    elif c == 1:
        print('焯！')
    elif c == 2:
        print('鬼！')
    else:
        print('我超，挂')  # 目前没有不开挂的方法能够触发这个
    __import__('os').system('pause')