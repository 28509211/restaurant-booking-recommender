import time

from opencc import OpenCC
# from translate import Translator
from google_trans_new import*
# from googletrans import Translator

def tw_2_zh(text):
    cc = OpenCC('t2s')
    data = (cc.convert(text))

    return data

def en_2_tw(text):
    # translator = Translator(to_lang="zh-TW")
    # translation = translator.translate(text)

    translator = google_translator(timeout=10)
    sample1 = text
    # 进行第一次翻译，目标是韩文
    translations = translator.translate(sample1, 'zh-tw')
    # 获得翻译结果
    return translations










# temp = []
# with open( 'test.txt', 'r', encoding='utf-8') as f :
#     r = f.readlines()
#     for i in r :
#         new_r = tw_2_zh(i)
#         temp.append(new_r)
#
# with open( 'test_zh.txt', 'w', encoding='utf-8') as f :
#     for i in temp :
#         f.write(i)

