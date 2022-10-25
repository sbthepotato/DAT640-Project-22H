import json
import re
import math
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
    """
    with open(filelocation, 'r', encoding='utf-8') as file:
        f = json.load(file)
        print('Successfully loaded ', filelocation)
        return f


def writeData(filelocation, dictionary):
    """Takes a filelocation and a dictionary and turns it into a json file
        have to make sure when making the dict that its the correct format.
    """
    # set the indent so that it looks pretty
    json_object = json.dumps(dictionary, indent=2)
    # open the file and write to it
    with open(filelocation, "w") as file:
        print('Writing to: ', filelocation)
        file.write(json_object)


def answerQuery(query, train):
    """Takes a question and the training dataset and finds the highest score match from the training dataset

    Returns the category, type and score of a question
    """
    queryP = preprocess(str(query))
    scoreA = -1.0
    categoryA = 'boolean'
    typeA = 'boolean'
    try:
        bm25 = BM25Okapi(queryP)
    except ZeroDivisionError as e:
        print('Zero division while creating instance')
        print(e)
        # in case of this error we'll just use a default category, type and score
        return categoryA, typeA, scoreA
    for j in train:
        scores = bm25.get_scores(j['question'])
        scoresSum = math.fsum(scores)
        if scoresSum > scoreA:
            scoreA = scoresSum
            categoryA = j['category']
            typeA = j['type']
    return categoryA, typeA, scoreA


def answerList(list_Q, train):
    """Takes a list of questions and a list of the training datasets
    and tries to classify the questions

    Returns a modified list
    """
    num_questions = len(list_Q)
    # ranges through the questions, we need the iterator to save answers to the list
    for i, j in enumerate(list_Q):
        # answer the question
        category, type, score = answerQuery(j['question'], train)
        # prints out the progress of question answering, taken from A2.1
        try:
            if (i + 1) % (num_questions // 100) == 0:
                print(f"{round(100*(i/num_questions))}% answered.")
        except:
            # sometimes with a reduced dataset this will freak out and break so we need to catch those errors
            print('something went wrong with the progress printout')
        list_Q[i]['category'] = category
        list_Q[i]['type'] = type
        list_Q[i]['score'] = score
    return list_Q
