import os
import pathlib
import sys
import getopt
import fnmatch
from string import printable
import codecs

def getDictionary(path):
    dictionaryArray = []
    with open(path) as f:
        for line in f:
            dictionaryArray.append(line)
            # dictionaryArray.append(stringArray[1])
    #         print(stringArray[1])
    # print(dictionaryArray)
    dictionaryArray = list(dict.fromkeys(dictionaryArray))
    return dictionaryArray


class match:
    def __init__(self, filename, wordmatch, linenumber, line):
        self.filename = filename
        self.wordmatch = wordmatch
        self.startlinenumber = linenumber
        self.endlinenumber = linenumber
        self.line = line

    def toString(self):
        return (self.filename, self.wordmatch, self.startlinenumber, self.endlinenumber, self.line)

def charStripper(input):
    try:
        # input = input.encode("ASCII", "ignore")
        input=input.replace('\n','')
        inputUpper = input.upper()
        inputUpper.encode('utf-8').strip().strip()
        inputUpper.replace("\n", "")
        # print(input)
        # print(inputUpper)
        output = ''.join(char for char in inputUpper if char in printable)
        # print(output)
        return output
    except Exception as ex:
        print("Error in normalizing the string: {}".format(input))
        print(ex)
        sys.exit(2)

def findMatches(sourceDirectory, dictionary):
    listOfMatches = []
    clearedLine = ''
    try:
        for root, dirs, files in os.walk(sourceDirectory, topdown=True):
            for name in fnmatch.filter(files, "*.csv"):
                checkpath = os.path.join(root, name)
                with open(checkpath) as checkfile:
                    for num, line in enumerate(checkfile, 1):
                        for word in dictionary:
                            # print(word)
                            word = charStripper(word)
                            if word.upper() in line.upper():
                                # print("{} in {} at {}".format(word, checkfile.name, num))
                                # matched=match(checkfile.name, word, num, line)
                                clearedLine = charStripper(line)
                                if clearedLine == '':
                                    break

                                matched = '{}^{}^{}^{}^"{}"'.format(checkfile.name, word, str(num), str(num), clearedLine)
                                print(matched)
                                listOfMatches.append(matched)

    except Exception as exc:
        print("Error: {}|{}".format(exc, word))
        print("Error: {}|{}".format(clearedLine, str(num)))
        sys.exit(2)

    print("Matches: {}".format(len(listOfMatches)))
    deduplicatedMatches = []
    for line in listOfMatches:
        if line not in deduplicatedMatches:
            deduplicatedMatches.append(line)
    print("deduplicated Matches: {}".format(len(deduplicatedMatches)))
    # for x in range(50):
    #     print(deduplicatedMatches[x])


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

    if (dictionary == '' or sourceDirectory == '' or outputFile == ''):
        print('All options are required. Use parser.py -h for help')
        sys.exit(2)

    print("Dictionary: ", dictionary)
    print("Source Code Directory", sourceDirectory)
    print("Output File", outputFile)

    Dictionary = getDictionary(dictionary)
    print('Length: ', str(len(Dictionary)))

    findMatches(sourceDirectory, Dictionary)


if __name__ == "__main__":
    main(sys.argv[1:])
