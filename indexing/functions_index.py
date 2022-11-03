import json
import re
import csv


def loadDatajson(filelocation):
    """Loads a json training dataset and returns it as a list of dictionaries.
    The keys are:

    'ID', 'question', 'category', 'type'
    """
    with open(filelocation, 'r', encoding='utf-8') as file:
        f = json.load(file)
        print('Successfully loaded ', filelocation)
        return f


def loadDataTurtle(filelocation):
    """Loads a ttf file and returns it as a list of lists with 2 items
    """
    with open(filelocation, 'r', encoding='utf-8') as file:
        retlist = []
        for line in file:
            sp = line.split(' ')
            entity = cleanUri(sp[0])
            type = cleanUri(sp[2])
            retlist.append([entity, type])
        return retlist


def writeDataTSV(filelocation, rows):
    """Takes a filelocation and a list and turns it into a tsv file
    """
    # field titles for clarity
    fields = ['INSTANCE', 'TYPE']
    # open the file and write to it
    with open(filelocation, "w") as file:
        print('Writing to: ', filelocation)
        # create writer
        tsvW = csv.writer(file, delimiter='\t')
        # write field titles
        tsvW.writerow(fields)
        # write the rows
        tsvW.writerows(rows)


def cleanUri(uri):
    """Cleans a uri and returns a cleaned version
    Adapted from A3.1
    """
    return preprocess(uri.split("/")[-1].replace("_", " ").replace('>', ''))


def preprocess(doc):
    """Preprocesses a document
    Taken from A2.1 assignment
    """
    return [term for term in re.sub(r"[^\w]|_", " ", doc).lower().split()]


def checkmatch(instanceTypes, questions, procNum, retDict):
    num = len(instanceTypes)
    for i in instanceTypes:
        ...


    retDict[procNum] = ...


