import json
import re
import nltk
import os 

from elasticsearch import Elasticsearch

# Global variables for multiprocessing
SPLITS = min(os.cpu_count(), 8)

# defines as a global variable for the multiprocessing
es = Elasticsearch(maxsize=128, timeout=64, max_retries=16, retry_on_timeout=True)


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


def answerList(quesList, procNum, retDict):
    """Answers a list of questions
    
    Takes a list of dictionaries with questions, a process number and a dictionary to return to

    returns a list of dicts with the answers
    """
    # length for progress print
    length = len(quesList)
    # range through the questions
    for i, j in enumerate(quesList):
        progressPrint(i, length, procNum)
        # answer the question
        category, type, score = answerQuery(j)
        # save the answers to the same list as used for input
        quesList[i]['category'] = category
        quesList[i]['type'] = type
        quesList[i]['score'] = score
    # reuturn
    retDict[procNum] = quesList


def answerQuery(question):
    """Answers a query using elasticsearch

    Takes a query

    Returns a category, type and score for the query
    """
    # preprocess the question to remove any special characters
    query = preprocess(str(question['question']))
    # default return values in case of some error
    qCategory = 'boolean'
    qType = 'boolean'
    qScore = -1.0

    # if the preprocess emptied the whole query
    if query == '':
        return qCategory, qType, qScore

    # use elasticsearch search to find the best match for the query with the built in BM25 scoring.
    # it first searches the training datasets that were indexed previously
    res = es.search(index='train', q=query, df="question", _source=False)['hits']['hits']

    # find the best matching document by its ID
    try:
        bestMatchDoc = es.get(id=res[0]['_id'], index='train')['_source']
    except Exception as e:
        # if it couldn't find it for whatever reason just return defaults
        print('Exception: ', e)
        return qCategory, qType, qScore

    # set the category, type and score
    qCategory = bestMatchDoc['category']
    qType = bestMatchDoc['type']
    qScore = res[0]['_score']

    # if its a resource then we will try to find types in the abstracts index
    if qCategory == 'resource':
        qType = resourceTypes(query)
    return qCategory, qType, qScore



def resourceTypes(query):
    """Searches the abstracts index for the best matching types for a resource

    Takes a query

    Returns a list of types
    """
    # search for the best match
    res = es.search(index='abstracts', q=query, df="description", _source=False, size=6)['hits']['hits']
    types = []
    # range through the top 6 results
    for i in range(6):
        # sometimes there are less than 6 results so we need to catch exceptions
        try:
            # takes the type from the top result
            qtype = (es.get(id=res[i]['_id'], index='abstracts')['_source']['type'])
            # for each type in the types 
            for j in qtype:
                # if it is not already a type and the total length of types in less than 6
                if j not in types and len(types) < 6:
                    # add the type
                    types.append(j)
        except Exception as e:
            print('Exception: ', e)
    return types
