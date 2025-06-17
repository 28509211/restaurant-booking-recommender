with open('reserve_train_data_system.txt') as f :
    h = f.readlines()


a = False
b = False
temp1 = []
count = 0
temp = []
all = []
s = ""
for i in h :

    if "<G>" in i :
        count = count + 1

    if count == 2 :

        if len(temp) == 1 :
            all.append(temp[0])
            if len(temp1) == 1 :
                all.append(temp1[0])
        else:
            for number, k in enumerate(temp) :
                if number + 1 != len(temp) and number + 1 != len(temp) - 1 :
                    k = k.strip()
                    k = k + "，"
                    s = s + k
                else:
                    if number + 1 == len(temp) - 1 :
                        k = k.strip()
                        s = s + k
                    else :
                        s = s + k

            all.append(s)

            s = ""
        a = False
        b = False
        temp = []
        temp1 = []
        count = 0

    if "<instruction>" in i :
        a = True


    if a :
        temp.append(i)
    else:
        all.append(i)



# for i in all :
#     print(i)


with open("test.txt", 'w', encoding='utf-8') as f:
    for i in all :
        f.write(i)

