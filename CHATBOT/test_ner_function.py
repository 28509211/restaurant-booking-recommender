def select_ner_type():
    ner_options = {
        1: "PEOPLE",
        2: "QUESTION",
        3: "FOOD",
        4: "ADJ",
        5: "ADDRESS",
        6: "DATE",
        7: "TIME",
        8: "TIME2",
        9: "STORE",
        10: "PLACE",
        0: "Skip"
    }
    
    # Display options
    print("選擇要添加的NER類型 (或按0跳過):")
    for key, value in ner_options.items():
        print(f"{key}. {value}")
    
    # Input choice
    choice = input("輸入選項號碼 (或直接按Enter跳過): ")
    
    if choice == "":  # User pressed Enter to skip
        return None
    else:
        choice = int(choice)  # Convert input to integer
        if choice in ner_options:
            return ner_options[choice]
        else:
            print("無效的選項，請重試")
            return select_ner_type()

def test_add_ner():
    test_ner = {}
    test_ner_type = select_ner_type()  # Let the user select an option from predefined NER types
    
    if test_ner_type and test_ner_type != "Skip":
        test_ner_data = input(f"輸入此輪要添加的NER單詞 {test_ner_type}: ")
        test_ner[test_ner_type] = test_ner_data
    else:
        print("跳過NER添加")
    
    return test_ner