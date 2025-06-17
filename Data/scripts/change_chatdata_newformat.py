import re

import re


def transform_text(input_text):
    # 用正则表达式匹配 <USER> 和 <BOT> 标签并在标签之间添加换行符
    transformed_text = re.sub(r'(<USER>[^<]*)(<BOT>)', r'\1\n\2', input_text)
    transformed_text = re.sub(r'(<BOT>[^<]*)(<USER>)', r'\1\n\2', transformed_text)

    # 在文本的开头和结尾添加 <G> 标签，并在结尾添加换行符
    transformed_text = f"<G>\n{transformed_text}\n<G>\n"

    return transformed_text


def main(input_file_path, output_file_path):
    # 从文件中读取输入文本
    with open(input_file_path, 'r', encoding='utf-8') as file:
        input_text = file.read()

    # 转换文本
    output_text = transform_text(input_text)

    # 将转换后的文本写入输出文件
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(output_text)

    print(f"Transformed text has been saved to {output_file_path}")


def main(input_file_path, output_file_path):
    # 从文件中读取输入文本
    with open(input_file_path, 'r', encoding='utf-8') as file:
        input_text = file.read()

    # 转换文本
    output_text = transform_text(input_text)

    # 将转换后的文本写入输出文件
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(output_text)

    print(f"Transformed text has been saved to {output_file_path}")


if __name__ == "__main__":
    # 输入文件路径
    input_file_path = 'chat_train_data.txt'
    # 输出文件路径
    output_file_path = 'chat_traindata_reserve_情況1.txt'

    # 运行主函数
    main(input_file_path, output_file_path)
