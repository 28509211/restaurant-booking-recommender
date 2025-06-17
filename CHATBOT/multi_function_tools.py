import itertools


def generate_combinations_permutations(lst ):

    r = len( lst )

    all_permutations = []

    for i in range(r) :

        combinations = itertools.combinations(lst, i+1)
        
        for combination in combinations:
            permutations = list(itertools.permutations(combination))
            all_permutations.extend(permutations)
        
    return all_permutations


def Label_For_Sequence( all_possible ) :

    all_possible_dict = {}
    number = 1
    last = 1

    for i in all_possible:

        # print( "now" + str(len(i)) )
        # print( "last" + str(last) )

        if len(i) == 1 :
            all_possible_dict[ i ] = 0
        elif len(i) != last :
            number = 1
            all_possible_dict[ i ] = bin( number )
            number = number + 1 
        else:
            all_possible_dict[ i ] = bin( number )
            number = number + 1 

        last = len(i)
        

    # print( all_possible_dict )

    return all_possible_dict

    
def Get_Binary_Address( binary ) :

    address = []
    binary = str(binary)
    reverse_binary = binary[::-1]

    for number, i in enumerate( reverse_binary ):
        if i == "1" :
            address.append( number + 1 )
        elif i == "b":
            break 


    return address

def Label_For_Sequence( all_possible ) :

    all_possible_dict = {}
    all_possible_dict[ ('聊天',) ] = 0
    number = 1
    last = 1

    for i in all_possible:

        # print( "now" + str(len(i)) )
        # print( "last" + str(last) )

        if len(i) == 1 :
            all_possible_dict[ i ] = 0
        elif len(i) != last :
            number = 1
            all_possible_dict[ i ] = bin( number )
            number = number + 1 
        else:
            all_possible_dict[ i ] = bin( number )
            number = number + 1 

        last = len(i)
        

    # print( all_possible_dict )

    return all_possible_dict


def Address_To_Bin( address_number ) :

    result = 0

    for num in address_number:
        result |= (1 << num)

    return bin(result)


def Create_MultiLabel_Dictionary( ) :
    
    temp = [ "訂位", "詢問", "導航", "推薦" ]
    all_possible = generate_combinations_permutations( temp )
   
    all_possible_dict = Label_For_Sequence( all_possible )
    classes =  ['聊天', '導航', '推薦', '訂位', '詢問', 1, 2, 3, 4, 5]

    answer = [0, 0, 0, 0, 0, 0, 0, 0 ,0, 0]

    label_dict = {}

    for i in all_possible_dict:
        for k in i:
            answer[ classes.index( k ) ] = 1
        
        address = Get_Binary_Address( all_possible_dict[i] )

        for k in address:
            answer[ classes.index( k ) ] = 1

        label_dict[ tuple( answer ) ] = i


        answer = [0, 0, 0, 0, 0, 0, 0, 0 ,0, 0]

    return label_dict
    # print( label_dict )




def Predict_Multi_Answer( predict ) :

    if len( predict ) == 1 :

        # print( predict[ 0 ] )

        return predict

    elif len( predict ) == 0 :

        return []

    else:

        temp = [ "訂位", "詢問", "導航", "推薦" ]
        all_possible = generate_combinations_permutations( temp )
        all_possible_dict = Label_For_Sequence( all_possible )

        result_key = {}

        # print( " sssssssssssssssss    +    ", predict)

        for key, value in all_possible_dict.items():
            if value == predict[-1]:  
                result_key[ len(key) ] = key 

        # print( "-------------------SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS" )
        # print( result_key )
        # print( "-------------------SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS" )
        if len( result_key ) != 0  :

            if len( predict ) - 1 in result_key :
                # print( result_key[ len( predict ) - 1 ] )

                return list( result_key[ len( predict ) - 1 ] )
            else :
                filtered_list = [item for item in predict if not item.isdigit()]

                return filtered_list
        else: 
            return []

        
