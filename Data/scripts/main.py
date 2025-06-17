from translatess import*
import re
from tqdm import tqdm

with open('有關reservedata.txt', 'r', encoding='utf-8') as f :
    data = f.readlines()



def transform_conversation(input_text):
    # Split the input text by <SEP>
    parts = input_text.split(" <SEP> ")

    # Initialize the transformed text with <G> at the beginning
    transformed_text = "<G>\n"

    # Mapping for labels
    label_map = {
        "Agent": "<BOT>",
        "User": "<USER>",
    }

    # Process each part
    for part in parts:
        # Split each part into label and text
        print(part)
        if part != '1 Table at " 8 Sushi " in Pacifica, for 2 people, Today at 6 pm' :
            label, text = part.split(": ", 1)
            transformed_label = label_map.get(label, label)
            transformed_text += f"{transformed_label}{text}\n"

    # Add closing <G> tag
    transformed_text += "<G>"

    return transformed_text


def transform_conversation2(input_text):
    # Split the input text by <SEP>
    parts = input_text.split(" <SEP> ")

    # Initialize the transformed text with <G> at the beginning
    transformed_text = "<G>\n"

    # Mapping for labels
    label_map = {
        "Agent": "<BOT>",
        "User": "<USER>",
        "USER": "<USER>"
    }

    # Process each part
    for part in parts:
        # Use regular expression to split only on the first occurrence of ": "
        match = re.match(r"^(Agent|User|USER):\s(.*)", part)
        if match:
            label, text = match.groups()
            transformed_label = label_map.get(label, label)
            transformed_text += f"{transformed_label}{text}\n"
        else:
            # In case the regex does not match, just add the original part (this should not normally happen)
            transformed_text += f"{part}\n"

    # Add closing <G> tag
    transformed_text += "<G>"

    return transformed_text


# Transform all conversations
transformed_texts = [transform_conversation2(text) for text in tqdm(data, desc="Processing parts")]

# Write the transformed conversations to a text file
output_file_path = '有關reservedata改.txt'
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for transformed_text in transformed_texts:
        output_file.write(transformed_text + "\n\n")  # Separate each conversation with an extra newline

print(f"Transformed conversations have been saved to {output_file_path}")

transformed_texts = [transform_conversation(text) for text in data]

