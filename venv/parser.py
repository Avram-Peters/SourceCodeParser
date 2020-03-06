import os
import pathlib
import sys
import getopt
import fnmatch



def getDictionary(path):
    dictionaryArray = []
    with open(path) as f:
        for line in f:
            stringArray = line.split(",")
            dictionaryArray.append(stringArray[1])
    #         print(stringArray[1])
    # print(dictionaryArray)
    return dictionaryArray

class match:
    def __init__(self, filename, wordmatch, linenumber):
        self.filename = filename
        self.wordmatch = wordmatch
        self.startlinenumber=linenumber
        self.endlinenumber=linenumber


def findMatches(sourceDirectory, dictionary):
    listOfMatches = []
    try:
        for root, dirs, files in os.walk(sourceDirectory, topdown=True):
            for name in fnmatch.filter(files, "*.csv"):
                checkpath = os.path.join(root, name)
                with open(checkpath) as checkfile:
                    for num, line in enumerate(checkfile, 1):
                        for word in dictionary:
                            # print(word)
                            if word in line:
                                # print("{} in {} at {}".format(word, checkfile.name, num))
                                matched=match(checkfile.name, word, num)
                                listOfMatches.append(matched)

    except:
        print ("Error: {}".format(checkfile))

    print(len(listOfMatches))
    listOfMatches = list(dict.fromkeys(listOfMatches))
    print(len(listOfMatches))


def main(argv):
    dictionary = ''
    sourceDirectory = ''
    outputFile = ''

    try:
        opts, args = getopt.getopt(argv, "hd:s:o:", ["help", "dictionary=", "source=", "output="])
    except getopt.GetoptError:
        print('parser.py -d <dictionary file> -s <source directory> -o <output file>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('parser.py -d <dictionary file> -s <source directory> -o <output file>')
            sys.exit()
        elif opt in ("-d", "--dictionary"):
            dictionary = arg
        elif opt in ("-s", "--source"):
            sourceDirectory = arg
        elif opt in ("-o", "--output"):
            outputFile = arg

    if (dictionary=='' or sourceDirectory =='' or outputFile ==''):
        print('All options are required. Use parser.py -h for help')
        sys.exit(2)

    print ("Dictionary: ", dictionary)
    print("Source Code Directory", sourceDirectory)
    print("Output File", outputFile)

    Dictionary = getDictionary(dictionary)
    print('Length: ', str(len(Dictionary)))

    findMatches(sourceDirectory, Dictionary)




if __name__ == "__main__":
    main(sys.argv[1:])
