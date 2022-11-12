import json
import re
import nltk


def preprocess(doc):
    """Preprocesses a document
    Taken from A2.1 assignment
    """
    ps = nltk.stem.PorterStemmer()
    return [ps.stem(term) for term in re.sub(r"[^\w]|_", " ", doc).lower().split()]


def loadData(filelocation):
    """Loads a JSON file

    Takes a filelocation as a string
    
    Returns the file as a list of dictionaries
    """
    with open(filelocation, 'r', encoding='utf-8') as file:
        f = json.load(file)
        print('Successfully loaded ', filelocation)
        return f


def writeData(filelocation, dictionary):
    """Write a JSON file

    Takes a list of dictionaries
    """
    # set the indent so that it looks pretty
    json_object = json.dumps(dictionary, indent=2)
    # open the file and write to it
    with open(filelocation, "w") as file:
        print('Writing to: ', filelocation)
        file.write(json_object)


def progressPrint(index, length, procnum):
    """Prints the current progress of processing something for a given process
    """
    try:
        if (index + 1) % (length // 100) == 0:
            print(f"{round(100*(index/length))}% processed. in process {procnum}")
    except:
        print('something went wrong with the progress printout in process', procnum)
