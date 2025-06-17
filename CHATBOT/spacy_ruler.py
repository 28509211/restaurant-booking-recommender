import spacy
import json 
from spacy.language import Language
from config import DATA_JSON

def Add_Ruler( nlp, label_type ) :
    with open( DATA_JSON, 'r', encoding='utf-8' ) as f :
        ruler_data = json.load( f ) 

    # nlp = spacy.load(r"./output1/model-best")
    ruler = nlp.add_pipe("entity_ruler")
    patterns = []

    for label, data_list in ruler_data.items():
        if label in label_type :
            for data in data_list:
                patterns.append({"label": label, "pattern": data})

    with nlp.select_pipes(enable="tagger"):
        ruler.add_patterns( patterns )

    return nlp   

