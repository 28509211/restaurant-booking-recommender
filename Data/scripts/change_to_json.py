import json
from translatess import *


def create_dialogue_json(dialogue_segments):
    conversations = []
    for segment in dialogue_segments:
        for role, utterance in segment:
            conversations.append({"from": role, "value": utterance.strip()})

    dialogue_json = {"conversations": conversations}
    return dialogue_json


# 从文件中读取对话内容
dialogue_segments = []
with open("test.txt", "r") as file:
    all = []
    times = 0
    lines = file.readlines()
    for i in lines :
        all.append(i.strip())

temp = []
system = ""
instruction = ""
for i in all :
    if i == "<G>":
        times = times + 1
    elif times == 2 :
        times = 0
        dialogue_segments.append([temp,system,instruction])
        temp = []
        system = ""
    else:
        if i == " " or i == "\n" or i == "":
            continue
        elif "<system>" in i:
            system = tw_2_zh(i)
        elif "<instruction>" in i:
            instruction = tw_2_zh(i)
        else:
            i = tw_2_zh(i)
            temp.append(i)

# print(dialogue_segments)


json_data = []  # 初始化 JSON 数据列表
system_info = ""
instruction_info = ""
conversation = []


for dialogue_segment in dialogue_segments:
    # print(dialogue_segment)
    for segment in dialogue_segment:  # 遍历每个对话段落
        print(segment)
#
#
        if "<system>"  not in segment and "<instruction>"  not in segment:
            for utterance in segment:  # 最后一个元素是系统信息，所以不包含在对话中

                try:
                    role, text = utterance.split('>', 1)
                    conversation.append({"from": role.strip('<'), "value": text.strip()})
                except ValueError:
                    # 如果无法按照 '>' 分割字符串，会触发 ValueError 异常
                    print("Error: Unable to split utterance:", utterance)
                    continue

        elif "<system>" in segment :
            system_info = segment.replace("<system>", "").strip()  # 获取系统信息并去除标签
        elif "<instruction>" in segment :
            instruction_info = segment.replace("<instruction>", "").strip()  # 获取系统信息并去除标签
#
            json_data.append({
                "conversations": conversation,
                "system": system_info,  # 使用提供的系统信息
                "instruction":instruction_info
            })  # 将对话列表及系统信息添加到 JSON 数据中

            conversation = []  # 初始化对话列表
            system_info = ""
            instruction_info = ""

print(json_data)
for i in json_data:
    print(i)

#
# # 最终得到的 json_data 就是包含所有对话段落的 JSON 数据列表
#
#
# # 将 JSON 数据写入文件
# with open('dialogue.json', 'w', encoding='utf-8') as f:
#     json.dump(json_data, f, ensure_ascii=False, indent=4)

