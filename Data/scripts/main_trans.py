import time
from translatess import *

with open('有關reservedata改.txt', 'r', encoding='utf-8') as f :
    all = f.readlines()

with open('有關reservedata改_zh.txt', 'r', encoding='utf-8') as f :
    alls = f.readlines()
    temp = len(alls)

with open('有關reservedata改_zh.txt', 'a', encoding='utf-8') as fe :
    for number, i in enumerate(all) :
        if number + 1 > temp :
            i = i .strip()
            print(i)
            try:
                time.sleep(10)
                i = en_2_tw(i)
                fe.write(i + '\n')
            except Exception as e:
                try:
                    # 執行 m.py
                    exec(open("translatess.py").read())
                except Exception as e:
                    print(f"Error executing m.py: {e}")