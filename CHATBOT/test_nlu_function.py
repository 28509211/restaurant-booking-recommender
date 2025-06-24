def select_nlu_type():
    nlu_options = {
        1: "聊天",
        2: "詢問",
        3: "推薦",
        4: "訂位",
        5: "導航",
    }
    
    # Display options
    print("選擇這輪的NLU功能:")
    for key, value in nlu_options.items():
        print(f"{key}. {value}")
    
    # Input choice
    choice = input("輸入選項號碼: ")
    
    choice = int(choice)  # Convert input to integer
    if choice in nlu_options:
        return nlu_options[choice]
    else:
        print("無效的選項，請重試")
        return select_ner_type()

def test_nlu():
    test_nlu_type = select_nlu_type()  # Let the user select an option from predefined NER types
    
    return test_nlu_type