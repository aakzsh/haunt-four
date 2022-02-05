


def listlist_to_stringlist(l):
    listy = []
    for i in l:
        s = ""
        for j in i:
            s+=str(j)
        listy.append(s)
    return listy

def stringlist_to_listlist(l):
    listy = []
    for i in l:
        temp = []
        for j in i:
            temp.append(int(j))
        listy.append(temp)

    return listy


def emojify(matrix):
    # print("mamamam", matrix)
    equivalent = {'0': '🔴','1':'🟡','2':'⬛'}
    emojified = ""
    for i in matrix:
        for j in i:
            emojified+=equivalent[j]
        emojified+="\n"
    emojified+="0️⃣1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣\n"

    return emojified







# print(listlist_to_stringlist([[1,1,1],[2,2,2],[3,3,3]]))

# print(stringlist_to_listlist(['111', '222', '333']))
    