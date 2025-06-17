import json
from translatess import *
def transform_to_json(data):
    system_prompt = ''
    instruction = []
    input_output_pairs = []
    times = 0
    all_result = []

    lines = data.strip().split('\n')
    for line in lines:
        line = tw_2_zh(line)
        if line.startswith("<G>"):
            times += 1
            if times == 2:
                conversations = []
                instruction_index = 0
                for i in range(0, len(input_output_pairs), 2):
                    user_input = input_output_pairs[i]
                    bot_output = input_output_pairs[i + 1] if (i + 1) < len(input_output_pairs) else None

                    if instruction_index < len(instruction):
                        human_value = instruction[instruction_index] + "\n" + user_input["content"]
                        instruction_index += 1
                    else:
                        human_value = user_input["content"]

                    conversations.append({
                        "from": "human",
                        "value": human_value
                    })

                    if bot_output:
                        conversations.append({
                            "from": "gpt",
                            "value": bot_output["content"]
                        })

                result = {
                    "conversations": conversations,
                    "system": system_prompt
                }

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
        elif line.startswith("<USER>"):
            user_input = line[len("<USER>"):].strip()
            input_output_pairs.append({"role": "USER", "content": user_input})
        elif line.startswith("<BOT>"):
            bot_output = line[len("<BOT>"):].strip()
            input_output_pairs.append({"role": "BOT", "content": bot_output})

    return all_result


with open('chat_traindata_reserve_情況6.txt', "r", encoding="utf-8") as f:
    data = f.read()

# print(data)

result_json = transform_to_json(data)



#
# # 将 JSON 数据写入文件
# output_file = "conversation.json"
with open('conversation6.json', 'w', encoding='utf-8') as f:
    json.dump(result_json, f, ensure_ascii=False, indent=4)
#
    print(f"已将数据保存到文件")