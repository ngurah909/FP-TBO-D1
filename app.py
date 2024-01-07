import graphviz
import streamlit as st
from graphviz import Source

TRIANGULAR_TABLE = {}
PARSE_TREE = None
PREV_NODE = None

RESULT = {}

def remove_unit_production(keyList):
    global RESULT
    for key, value in RESULT.items():
        if key in keyList:
            tempList = []
            for prod in value:
                if len(prod.split(" ")) == 2:
                    tempList.append(prod)
                else:
                    for i in RESULT[prod]:
                        if i not in tempList:
                            tempList.append(i)
            RESULT[key] = tempList

def get_set_of_production():
    global RESULT
    RESULT.clear()
    f = open("./set_of_production.txt", "r", encoding="utf-8")
    for lines in f:
        line = lines.splitlines()
        line = line[0].split(" -> ")
        lhs = line[0]
        rhs = line[1].split(" | ")
        if lhs in RESULT.keys():
            RESULT[lhs].extend(rhs)
        else:
            RESULT[lhs] = rhs
    f.close()
    for key, value in RESULT.items():
        if key == "PropNoun":
            tempList = []
            for val in value:
                if val not in tempList:
                    tempList.append(val.lower())
            RESULT[key] = tempList
    phrases = ["NumP", "AdvP", "AdjP", "PP", "NP", "VP"]
    remove_unit_production(phrases)
    patterns = ["S", "P", "O", "Pel", "Ket"]
    remove_unit_production(patterns)
    tempList = []
    tempDict = {}
    counter = 1
    for key, value in RESULT.items():
        if key == "K":
            for val in value:
                if len(val.split(" ")) > 2:
                    temp = val.split(" ")
                    while len(temp) > 2:
                        checkStr = temp[0] + " " + temp[1]
                        isFound = False
                        for k, v in tempDict.items():
                            if checkStr == v:
                                isFound = True
                                temp.pop(0)
                                temp.pop(0)
                                temp.insert(0, k)
                                break
                        if not isFound:
                            tempDict["K" + str(counter)] = checkStr
                            temp.pop(0)
                            temp.pop(0)
                            temp.insert(0, "K" + str(counter))
                            counter += 1
                    tempList.append(" ".join(temp))
                else:
                    tempList.append(val)
            RESULT[key] = tempList
    for key, value in tempDict.items():
        RESULT[key] = [value]
    return RESULT

def get_raw_set_of_production():
    global RESULT
    RESULT.clear()
    f = open("./set_of_production.txt", "r", encoding="utf-8")
    for lines in f:
        line = lines.splitlines()
        line = line[0].split(" -> ")
        lhs = line[0]
        rhs = line[1].split(" | ")
        if lhs in RESULT.keys():
            RESULT[lhs].extend(rhs)
        else:
            RESULT[lhs] = rhs
    f.close()
    for key, value in RESULT.items():
        if key == "PropNoun":
            tempList = []
            for val in value:
                if val not in tempList:
                    tempList.append(val.lower())
            RESULT[key] = tempList
    tempList = []
    tempDict = {}
    counter = 1
    for key, value in RESULT.items():
        if key == "K":
            for val in value:
                if len(val.split(" ")) > 2:
                    temp = val.split(" ")
                    while len(temp) > 2:
                        checkStr = temp[0] + " " + temp[1]
                        isFound = False
                        for k, v in tempDict.items():
                            if checkStr == v:
                                isFound = True
                                temp.pop(0)
                                temp.pop(0)
                                temp.insert(0, k)
                                break
                        if not isFound:
                            tempDict["K" + str(counter)] = checkStr
                            temp.pop(0)
                            temp.pop(0)
                            temp.insert(0, "K" + str(counter))
                            counter += 1
                    tempList.append(" ".join(temp))
                else:
                    tempList.append(val)
            RESULT[key] = tempList
    for key, value in tempDict.items():
        RESULT[key] = [value]
    return RESULT

def is_accepted(inputString):
    global TRIANGULAR_TABLE
    TRIANGULAR_TABLE.clear()
    prodRules = get_set_of_production()
    inputString = inputString.lower().split(" ")
    for i in range(1,len(inputString)+1):
        for j in range(i, len(inputString)+1):
            TRIANGULAR_TABLE[(i,j)] = []
    for i in reversed(range(1, len(inputString)+1)):
        for j in range(1, i+1):
            if (j == j + len(inputString) - i):
                tempList = []
                for key, value in prodRules.items():
                    for val in value:
                        if (val == inputString[j-1] and key not in tempList):
                            tempList.append(key)
                TRIANGULAR_TABLE[(j, j + len(inputString) - i)] = tempList
            else:
                tempList = []
                resultList = []
                for k in range(len(inputString) - i):
                    first = TRIANGULAR_TABLE[(j,j+k)]
                    second = TRIANGULAR_TABLE[(j+k+1,j+len(inputString) - i)]
                    for fi in first:
                        for se in second:
                            if (fi + " " + se not in tempList):
                                tempList.append(fi + " " + se)
                for key, value in prodRules.items():
                    for val in value:
                        if (val in tempList and key not in resultList):
                            resultList.append(key)
                TRIANGULAR_TABLE[(j,j+len(inputString) - i)] = resultList
    if "K" in TRIANGULAR_TABLE[(1, len(inputString))]:
        return True
    else:
        return False

def is_parent(posX, posY, limit, check, prodRules):
    global TRIANGULAR_TABLE
    x = posX
    y = posY
    while posX > 1 and posY <= limit:
        posX -= 1
        if TRIANGULAR_TABLE[(posX, posY)] != []:
            backVar = TRIANGULAR_TABLE[(posX, posY)][-1]
            for i in prodRules[backVar]:
                if check in i.split(" "):
                    return [True, posX, posY]
            return [False, None, None]
    posX = x
    posY = y
    while posX >= 1 and posY < limit:
        posY += 1
        if TRIANGULAR_TABLE[(posX, posY)] != []:
            backVar = TRIANGULAR_TABLE[(posX, posY)][-1]
            for i in prodRules[backVar]:
                if check in i.split(" "):
                    return [True, posX, posY]
            return [False, None, None]
    return [False, None, None]

def search_left(listVar, checkPos, curPost, posX, posY, limit, prodRules):
    global PARSE_TREE
    global PREV_NODE

    structureTier = ["S", "P", "O", "Pel", "Ket"]

    if len(listVar) == 1:
        if (listVar[0] == "K"):
            PARSE_TREE.edge("K", PREV_NODE)
            return
        else:
            res, x, y = is_parent(posX, posY, limit, listVar[curPost], prodRules)
            if res == True:
                temp = TRIANGULAR_TABLE[(x, y)][-1]
                parentNode = str(temp + " (" + str(x) + "," + str(y) + ")")
                PARSE_TREE.edge(parentNode, PREV_NODE)
                PREV_NODE = parentNode
                search_left(TRIANGULAR_TABLE[(x, y)], len(TRIANGULAR_TABLE[(x, y)])-2, len(TRIANGULAR_TABLE[(x, y)])-1, x, y, limit, prodRules)
            else:
                return
    else:
        if listVar[checkPos] in structureTier and checkPos == 0:
            res, x, y = is_parent(posX, posY, limit, listVar[checkPos], prodRules)
            if res == True:
                parentNode = str(listVar[checkPos] + " (" + str(posX) + "," + str(posY) + ")")
                PARSE_TREE.edge(parentNode, PREV_NODE)
                PREV_NODE = parentNode
                PARSE_TREE.edge("K", parentNode)
                return
            else:
                res2, x2, y2 = is_parent(posX, posY, limit, listVar[curPost], prodRules)
                if res2 == True:
                    temp = TRIANGULAR_TABLE[(x2, y2)][-1]
                    parentNode = str(temp + " (" + str(x2) + "," + str(y2) + ")")
                    PARSE_TREE.edge(parentNode, PREV_NODE)
                    PREV_NODE = parentNode
                    search_left(TRIANGULAR_TABLE[(x2, y2)], len(TRIANGULAR_TABLE[(x2, y2)])-2, len(TRIANGULAR_TABLE[(x2, y2)])-1, x2, y2, limit, prodRules)
                else:
                    return
        
        elif listVar[checkPos] in structureTier and checkPos > 0:
            res, x, y = is_parent(posX, posY, limit, listVar[checkPos], prodRules)
            if res == True:
                parentNode = str(listVar[checkPos] + " (" + str(posX) + "," + str(posY) + ")")
                PARSE_TREE.edge(parentNode, PREV_NODE)
                PREV_NODE = parentNode
                search_left(TRIANGULAR_TABLE[(x, y)], len(TRIANGULAR_TABLE[(x, y)])-2, len(TRIANGULAR_TABLE[(x, y)])-1, x, y, limit, prodRules)
            else:
                search_left(listVar, checkPos-1, curPost, posX, posY, limit, prodRules)
        
        elif listVar[checkPos] not in structureTier and checkPos == 0:
            parentNode = str(listVar[checkPos] + " (" + str(posX) + "," + str(posY) + ")")
            PARSE_TREE.edge(parentNode, PREV_NODE)
            PREV_NODE = parentNode
            res, x, y = is_parent(posX, posY, limit, listVar[checkPos], prodRules)
            if res:
                temp = TRIANGULAR_TABLE[(x, y)][-1]
                parentNode = str(temp + " (" + str(x) + "," + str(y) + ")")
                PARSE_TREE.edge(parentNode, PREV_NODE)
                PREV_NODE = parentNode
                search_left(TRIANGULAR_TABLE[(x, y)], len(TRIANGULAR_TABLE[(x, y)])-2, len(TRIANGULAR_TABLE[(x, y)])-1, x, y, limit, prodRules)
        
        elif listVar[checkPos] not in structureTier and checkPos > 0:
            isFound = False
            for i in prodRules[listVar[checkPos]]:
                if listVar[curPost] in i.split(" "):
                    parentNode = str(listVar[checkPos] + " (" + str(posX) + "," + str(posY) + ")")
                    PARSE_TREE.edge(parentNode, PREV_NODE)
                    PREV_NODE = parentNode
                    isFound = True
                    break
            if isFound:
                search_left(listVar, checkPos-1, checkPos, posX, posY, limit, prodRules)

def get_parse_tree(inputString):
    if is_accepted(inputString):
        global TRIANGULAR_TABLE
        global PARSE_TREE
        global PREV_NODE

        PARSE_TREE = graphviz.Graph("G", strict=True)
        PARSE_TREE.attr("node", shape="circle")
        PARSE_TREE.node("K")

        prodRules = get_raw_set_of_production()
        inputString = inputString.lower().split(" ")

        for i in range(1, len(inputString)+1):
            baseList = TRIANGULAR_TABLE[(i, i)]
            childNode = str(inputString[i-1] + " (" + str(i) + "," + str(i) + ")")
            parentNode = str(baseList[-1] + " (" + str(i) + "," + str(i) + ")")
            PARSE_TREE.edge(parentNode, childNode)
            PREV_NODE = parentNode
            if (len(baseList) == 1):
                search_left(baseList, len(baseList)-1, len(baseList)-1, i, i, len(inputString), prodRules)
            else:
                search_left(baseList, len(baseList)-2, len(baseList)-1, i, i, len(inputString), prodRules)
        return PARSE_TREE
    else:
        return None

def get_table_element(inputString):
    global TRIANGULAR_TABLE
    result = []
    n = len(inputString.split(" "))
    for i in range(1, n+1):
        temp = []
        for j in range(i):
            res = TRIANGULAR_TABLE[(j+1, n-i+j+1)]
            if len(res) == 0:
                temp.append("\u2205")
            else:
                temp.append("{" + ", ".join(res) + "}")
        result.append(temp)
    result.append(inputString.split(" "))
    return result

def main():
    st.title("Aplikasi Parsing Kalimat Baku Berbahasa Indonesia")
    st.markdown("""
    <div style="text-align: justify;">
    Aplikasi ini merupakan aplikasi yang digunakan untuk melakukan parsing kalimat berbahasa indonesia dengan pola kalimat sederhana sesuai dengan pedoman Umum Ejaan Bahasa Indonesia (PUEBI) dan Tata Bahasa Baku Bahasa Indonesia Edisi Keempat.
    </div> <br>
    """, unsafe_allow_html=True)

    input_string = st.text_input("Masukan kalimat untuk diparsing:")

    if st.button("Parse"):
        parse_tree = get_parse_tree(input_string)
        triangular_table = get_table_element(input_string)

        if parse_tree is not None:
            #st.subheader("Parse Tree:")
            #st.graphviz_chart(parse_tree)

            st.markdown(
            f"""<div style="background-color: #8AFF8A; padding: 10px; border-radius: 10px; text-align: center;">
            Berdasarkan hasil pemeriksaan, <span style="font-weight: bold;">{input_string}</span><br>
           <span style="font-weight: bold; color: #07AC17;">VALID</span><br>
            Sesuai dengan pola dasar bahasa Indonesia
            </div>""",
            unsafe_allow_html=True
            )
            
            st.subheader("Triangular Table:")
            st.table(triangular_table[:-1])  # Display the table without the last row

        else:
            st.markdown(
            f"""<div style="background-color: #FF8A8A; padding: 10px; border-radius: 10px; text-align: center;">
            Berdasarkan hasil pemeriksaan, <span style="font-weight: bold;">{input_string}</span><br>
           <span style="font-weight: bold; color: #D81717;">TIDAK VALID</span><br>
            Tidak sesuai dengan pola dasar bahasa Indonesia
            </div>""",
            unsafe_allow_html=True
            )

if __name__ == "__main__":
    main()