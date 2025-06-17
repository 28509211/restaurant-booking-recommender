import json
from translatess import *
def transform_to_json(data):
    system_prompt = ''
    instruction = []
    input_output_pairs = []
    times = 0
    all_result = []
    instruction_count = 0

    lines = data.strip().split('\n')
    for line in lines:
        line = tw_2_zh(line)
        if line.startswith("<G>"):
            times = times + 1
            if times == 2:
                count = 0
                history = []
                for i in range(0, len(input_output_pairs) - 1, 2):
                    history.append([
                        f"{instruction[count]}\n{input_output_pairs[i]['content']}",
                        input_output_pairs[i + 1]['content']
                    ])
                    count = count + 1

                print(input_output_pairs)

                last_bot= input_output_pairs[-1]['content']
                last_user = input_output_pairs[-2]['content']

                history.remove(history[-1])

                result = ({
                    'instruction': instruction[-1],
                    'input': last_user,
                    'output': last_bot,
                    'system': system_prompt,
                    'history': history
                })

                all_result.append(result)

                system_prompt = ''
                instruction = []
                input_output_pairs = []
                times = 0

        elif line.startswith("<system>"):
            system_prompt = line[len("<system>"):].strip()
        elif line.startswith("<instruction>"):
            instruction_content = line[len("<instruction>"):].strip()
            instruction.append(instruction_content)
            instruction_count = instruction_count + 1
        elif line.startswith("<USER>"):
            user_input = line[len("<USER>"):].strip()
            input_output_pairs.append({"role": "USER", "content": user_input})
        elif line.startswith("<BOT>"):
            bot_output = line[len("<BOT>"):].strip()
            input_output_pairs.append({"role": "BOT", "content": bot_output})

    return all_result


with open('chat_traindata_reserve_情況7.txt', "r", encoding="utf-8") as f:
    data = f.read()

# print(data)

result_json = transform_to_json(data)



#
# # 将 JSON 数据写入文件
# output_file = "conversation.json"
with open('conversation7.json', 'w', encoding='utf-8') as f:
    json.dump(result_json, f, ensure_ascii=False, indent=4)
#
    print(f"已将数据保存到文件")