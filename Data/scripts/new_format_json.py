import json


def transform_json(input_json):
    transformed_data = []

    for record in input_json:
        instruction = record.get("instruction", "")
        system = record.get("system", "")
        conversations = record.get("conversations", [])
        history = []

        # 填充历史对话
        for i in range(0, len(conversations) - 2, 2):
            # 拼接 human_value
            input_value = conversations[i]["value"] if i < len(conversations) else ""
            human_value = f"{instruction}\n{input_value}"
            gpt_value = conversations[i + 1]["value"] if i + 1 < len(conversations) else ""
            history.append([human_value, gpt_value])

        # 获取最后一轮对话
        if len(conversations) >= 2:
            input_value = conversations[-2]["value"]
            output_value = conversations[-1]["value"]
            last_human_value = input_value  # 只保留最后一轮对话的 input 内容
        else:
            input_value = ""
            output_value = ""
            last_human_value = ""

        transformed_record = {
            "instruction": instruction,
            "input": last_human_value,
            "output": output_value,
            "system": system,
            "history": history
        }
        transformed_data.append(transformed_record)

    return transformed_data

if __name__ == "__main__":
    # 输入JSON文件路径
    input_file_path = 'dialogue.json'
    # 输出JSON文件路径
    output_file_path = 'dialogue_format2.json'

    # 从文件中读取输入JSON数据
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        input_data = json.load(input_file)

    # 转换数据
    transformed_data = transform_json(input_data)

    # 保存转换后的数据到输出JSON文件
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(transformed_data, output_file, ensure_ascii=False, indent=2)

    print(f"Transformed JSON has been saved to {output_file_path}")
