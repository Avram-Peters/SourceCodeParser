import os
import pathlib
import sys
import getopt
import fnmatch
from string import printable
import codecs
import datetime

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


def charStripper(input):
    # Transforms strings to upper case, removes unprintable characters, and strips start/end white spaces. Returns the string
    try:
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

def writecontext(filename, linenumber, foundword, outputfile):
    # Writes the context of the found word to a file
    # (context = +/- five lines from the find)
    startIndex = max(0, linenumber - 5)

    with open(outputfile, "a+") as outfile:
        with open(filename, "r+") as infile:
            lines = infile.readlines()
            endIndex = min(len(lines) - 1, linenumber + 5)
            outfile.write("Word: {}\n".format(foundword))
            outfile.write("Line Number: {}\n".format(str(linenumber)))
            outfile.writelines(lines[startIndex: endIndex])
            outfile.write("\n")


def findMatches(sourceDirectory, dictionary, filetype, outputfile):
    # finds the matches and processes them

    # initiate output file
    epochdate = datetime.datetime.today()
    filename = "{}.{}{}{}{}{}{}.txt".format(outputfile,
                                        epochdate.year,
                                        epochdate.month,
                                        epochdate.day,
                                        epochdate.hour,
                                        epochdate.minute,
                                        epochdate.second
    )
    open(filename, "w+")

    listOfMatches = []
    clearedLine = ''
    filetype = "*.{}".format(filetype)
    try:
        # iterate through the source directory
        for root, dirs, files in os.walk(sourceDirectory, topdown=True):
            # iterate through the directory, looking for specified file types
            for name in fnmatch.filter(files, filetype):
                checkpath = os.path.join(root, name)
                # Opens the file, and iterates through the dictionary file
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
                                    continue
                                # Print the matched line
                                matched = '{}^{}^{}^{}^"{}"'.format(checkfile.name, word, str(num), str(num), clearedLine)
                                print(matched)

                                #send the match to the writecontext, to log in the output file
                                writecontext(checkfile.name, num, word, filename)
                                listOfMatches.append(matched)

                                # Stop iterating through the dictionary if one match if found.
                                # This reduces duplicated matches when one word in the dictionary is found multiple times.
                                # (AVAILABLE, ABLE, AVAIL) all would match in a single line, and is redundant.

                                break
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
    fileType = ''

    try:
        opts, args = getopt.getopt(argv, "hd:s:o:t:", ["help", "dictionary=", "source=", "output=", "type="])
    except getopt.GetoptError:
        print('parser.py -d <dictionary file> -s <source directory> -o <output file> -t <file suffix>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('parser.py -d <dictionary file> -s <source directory> -o <output file> -t <file suffix>')
            sys.exit()
        elif opt in ("-d", "--dictionary"):
            dictionary = arg
        elif opt in ("-s", "--source"):
            sourceDirectory = arg
        elif opt in ("-o", "--output"):
            outputFile = arg
        elif opt in ("-t", "--filetype"):
            fileType = arg

    if (dictionary == '' or sourceDirectory == '' or outputFile == '' or fileType == ''):
        print('All options are required. Use parser.py -h for help')
        sys.exit(2)

    print("Dictionary: ", dictionary)
    print("Source Code Directory: ", sourceDirectory)
    print("Output File: ", outputFile)
    print("File Type: ", fileType)
    Dictionary = getDictionary(dictionary)
    print('Length: ', str(len(Dictionary)))

    findMatches(sourceDirectory, Dictionary, fileType, outputFile)


if __name__ == "__main__":
    main(sys.argv[1:])
