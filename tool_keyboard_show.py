from msvcrt import getch

while True:
    ch = getch()
    print(f'{ord(ch)}({repr(ch)})')