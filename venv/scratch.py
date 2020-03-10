import os

def getDictionary(input, output):
    dictionaryArray = []
    with open(input) as f:
        for line in f:
            stringArray = line.split(",")
            dictionaryArray.append(stringArray[1])
    #         print(stringArray[1])
    # print(dictionaryArray)

    dictionaryArray = list(dict.fromkeys(dictionaryArray))
    with open(output, "w+") as f2:
        for item in dictionaryArray:
            if item != 'Amazon' and len(item) > 3:
                f2.write("{}\n".format(item))
    return dictionaryArray


inputpath = "/Users/ajp0423/Downloads/nouns.csv"
outputpath = "/Users/ajp0423/Downloads/nouns.txt"
getDictionary(inputpath, outputpath)
