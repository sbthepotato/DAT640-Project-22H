import json
import re
import nltk
from elasticsearch import Elasticsearch

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




#######################################
#                                     #
# The functions below this point are  #
# used to actually answer the dataset #
#                                     #
#######################################

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
        category, type, score, query = answerQuery(j)
        # save the answers to the same list as used for input
        quesList[i]['question'] = query
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

    # if the preprocess emptied the whole query
    if len(query) == 0:
        print('questionID: ', question['id'], ' is empty after preprocess')
        return 'resource', ['dbo:Thing'], -1.0, ' '.join(query)

    # use elasticsearch search to find the best match for the query with the built in BM25 scoring.
    # it first searches the training datasets that were indexed previously
    res = es.search(index='train', q=query, df="question", _source=False)['hits']['hits']

    # find the best matching document by its ID
    bestMatchDoc = es.get(id=res[0]['_id'], index='train')['_source']

    # set the category, type and score
    qCategory = bestMatchDoc['category']
    qType = bestMatchDoc['type']
    qScore = res[0]['_score']

    # if its a resource then we will try to find types in the abstracts index
    if qCategory == 'resource':
        qType = resourceTypes(query)
    return qCategory, qType, qScore, ' '.join(query)


def resourceTypes(query):
    """Searches the abstracts index for the best matching types for a resource

    Takes a query

    Returns a list of types
    """
    # search for the 20 best matches
    res = es.search(index='abstracts', q=query, df="description", _source=False, size=20)['hits']['hits']
    types = []
    # range through the results
    for i in res:
        # takes the type from the top result
        qtype = es.get(id=i['_id'], index='abstracts')['_source']['type']
        # for each type in the types 
        for j in qtype:
            # if it is not already a type and the total length of types is less than 10
            if j not in types and len(types) < 10:
                # add the type
                types.append(j)
    types = dboResourceTypes(types)
    return types


def dboResourceTypes(types):
    """Adds 'dbo:' to the start of the resource types
    
    Takes a list of types

    Returns a list of types with 'dbo:' at the start of each type
    """
    converted = []
    for i in types:
        converted.append('dbo:' + i)
    return converted
