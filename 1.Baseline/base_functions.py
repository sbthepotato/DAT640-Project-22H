import json
from rank_bm25 import BM25

def loadData(filelocation):
    """Loads a json training dataset and returns it as a list of dictionaries.
    The keys are:

    'ID', 'question', 'category', 'type'
    
    Note: 'Boolean' category have no type
    """
    with open(filelocation, 'r', encoding='utf-8') as file:
        return json.load(file)


def writeData(filelocation, dictionary):
    """Takes a filelocation and a dictionary and turns it into a json file
        have to make sure when making the dict that its the correct format.
    """
    json_object = json.dumps(dictionary, indent=4)
    # could also do this but the current one is more readable
    # json.dump(dictionary, file)
    with open(filelocation, "w") as file:
        file.write(json_object)

def rankQuery(query, questions):
    BM25(query)

