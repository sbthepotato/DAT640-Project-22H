import json
import re
from rank_bm25 import BM25Okapi

def preprocess(doc):
    """Preprocesses a question
    Taken from A2.1 assignment
    """
    return [
        term for term in re.sub(r"[^\w]|_", " ", doc).lower().split()
    ]

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

def answerQuery(query, train):
    """Takes a question and the training dataset and finds the highest score match from the training dataset
    """
    bm25 = BM25Okapi(query)
    score = 0
    categoryA = ''
    typeA = ''
    for j in train:
        ques = j['question']
        scores = bm25.get_scores(ques)
        if scores[0] > score:
            score = scores[0]
            categoryA = j['category']
            typeA = j['type']
       
    return categoryA, typeA


