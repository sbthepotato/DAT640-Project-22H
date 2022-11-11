import json
import re
import math
import rank_bm25
import nltk
import datetime


def preprocess(doc):
    """Preprocesses a document
    Taken from A2.1 assignment
    """
    ps = nltk.stem.PorterStemmer()
    return [ps.stem(term) for term in re.sub(r"[^\w]|_", " ", doc).lower().split()]


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


def progressPrint(index, length, procnum):
    """Prints the current progress of processing something for a given process
    """
    try:
        if (index + 1) % (length // 100) == 0:
            print(f"{round(100*(index/length))}% processed. in process {procnum}")
    except:
        print('something went wrong with the progress printout in process', procnum)


def splitFunc(a, n):
    """splits list 'a' into 'n' pieces

    returns a Generator which needs to be converted back to a list

    from: https://stackoverflow.com/a/2135920
    """
    if n == 1:
        return a
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))


def answerQuery(query, train, procNum):
    """Takes a question and the training dataset and finds the highest score match from the training dataset

    Returns the category, type and score of a question
    """
    query = preprocess(str(query['question']))
    scoreA = -1.0
    categoryA = 'boolean'
    typeA = 'boolean'
    # catch zerodivision errors to avoid termination
    try:
        bm25 = rank_bm25.BM25Okapi(query)
    except ZeroDivisionError as e:
        print('Zero division while creating instance in process ', procNum)
        print('Question id: ', query['id'])
        print(e)
        # we'll just use a default category, type and score
        return categoryA, typeA, scoreA
    # iterate through the training dataset
    for j in train:
        # compare the query to the entry in the training dataset
        scores = bm25.get_scores(j['question'])
        # sum the score and compare if it has improved
        scoresSum = math.fsum(scores)
        if scoresSum > scoreA:
            scoreA = scoresSum
            categoryA = j['category']
            typeA = j['type']
    return categoryA, typeA, scoreA


def answerList(quesList, train, procNum, retDict):
    """Takes a list of questions, a list of the training dataset, the process number and the dictionary it will return
    and tries to classify the questions

    Returns a dictionary with the process id as key with the modified input list as value
    """
    num_questions = len(quesList)
    # ranges through the questions, we need the iterator to save answers to the list
    for i, j in enumerate(quesList):
        # prints out the progress of question answering, taken from A2.1
        progressPrint(i, num_questions, procNum)
        # answer the question
        category, type, score = answerQuery(j, train, procNum)
        # add the category, type and score to the current question entry
        quesList[i]['category'] = category
        quesList[i]['type'] = type
        quesList[i]['score'] = score
    # return the dict with the process number as key
    retDict[procNum] = quesList


# going to be replaced
def findTypeIDList(quesList, bm25object):
    length = len(quesList)
    for i, j in enumerate(quesList):
        progressPrint(i, length, 0)
        if j['category'] == 'resource':
            print('started resource', datetime.datetime.now())
            idx = 0
            scoreT = -1.0
            best = bm25object.get_top_n(tokenized_query, corpus, n=1)
            for k, m in enumerate(scores):
                if m > scoreT:
                    idx = k
                    scoreT = m
            quesList[i]['typeID'] = idx
            quesList[i]['scoreType'] = scoreT
            print('finished resource', datetime.datetime.now())
    return quesList
