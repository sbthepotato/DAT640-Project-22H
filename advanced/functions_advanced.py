from functions_base import *
from elasticsearch import Elasticsearch

# defines as a global variable for the multiprocessing
es = Elasticsearch(maxsize=128, timeout=64, max_retries=16, retry_on_timeout=True)


# unchanged from baseline
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
    resultDocs = []
    try:
        for i in range(5):
            resultDocs.append(es.get(id=res[i]['_id'], index='train')['_source'])
    except Exception as e:
        # if it couldn't find it for whatever reason just return defaults
        print('Exception: ', e)
        if len(resultDocs) >= 1:
            return resultDocs[0]['category'], resultDocs[0]['type'], res[0]['_score']
        return qCategory, qType, qScore

    # set the category, type and score
    qCategory, qType, qScore = sortResults(resultDocs, res)


    # if its a resource then we will try to find types in the abstracts index
    if qCategory == 'resource':
        qType = resourceTypes(query)
    return qCategory, qType, qScore


def sortResults(results, res):
    ...
    optionsDict = {'resource':[],'literal':[],'boolean':[]}
    for i, j in enumerate(results):
        if j['type'] == 'resource':
            optionsDict['resource'] = j, res[i]
        elif j['type'] == 'literal':
            optionsDict['literal'] = j, res[i]
        elif j['type'] == 'boolean':
            optionsDict['boolean'] = j, res[i]





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








# OLD STUFF
"""
 def scoreQuery(bm25, train):
    #Takes the bm25 class and the training dataset and finds the highest score match from each category

    #Returns a dict of dicts for each category (resource, literal, boolean)
    
    optionsDict = {'resource':{},'literal':{},'boolean':{}}
    for j in train:
        # compare the query to the entry in the training dataset
        scores = bm25.get_scores(j['question'])
        # sum the score and compare if it has improved
        scoresSum = math.fsum(scores)
        # update the options dict with the score (or not, depends)
        optionsDict = updateHighest(j, scoresSum, optionsDict)
    return optionsDict


def updateHighest(trainQuery, score, optionsDict):
    #Takes the current query from the training dataset, the score it got and the options dict and updates the option dict
    
    #Returns the updated optionsDict (same one as given as input)
    
    # check the category of the train query
    if trainQuery['category'] == 'boolean':
        # if the score is higher than what we saw before for the category
        if score > optionsDict['boolean']['score']:
            # update the key in the dict
            optionsDict['boolean'] = {'type':trainQuery['type'],'score':score, 'question':trainQuery['question']}
    elif trainQuery['category'] == 'literal':
        if score > optionsDict['literal']['score']:
            optionsDict['literal'] = {'type':trainQuery['type'],'score':score, 'question':trainQuery['question']}
    elif trainQuery['category'] == 'resource':
        if score > optionsDict['resource']['score']:
            # TODO: handle wikidata entries having different types
            optionsDict['resource'] = {'type':trainQuery['type'],'score':score, 'question':trainQuery['question']}
    return optionsDict


def classifyQuery(answers):
    #Doesnt do anything special yet but will:
    #takes the optionsDict with the highest performing answers for each category and modifies the scores to try to improve the match

    #Returns the highest score category, types and its score
    
    # TODO: This whole thing
    scoreA = -1.0
    categoryA = 'boolean'
    typeA = 'boolean'

    for i, j in answers.items():
        if j['score'] > scoreA:
            categoryA = i
            typeA = j['type']
    return categoryA, typeA, scoreA
     """
    
