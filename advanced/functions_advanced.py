from functions_base import *
from elasticsearch import Elasticsearch

# defines as a global variable for the multiprocessing
es = Elasticsearch(maxsize=128, timeout=64, max_retries=16, retry_on_timeout=True)




############################
# Unchanged from baseline  #
############################
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




#####################################
#  Functions changed from baseline  #
#####################################
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

    # checks if the query contains 'how many', many is mani due to preprocessing
    if checkForTermSequence(query, 'how', 'mani'):
        return 'literal', ['number'], 69.0, ' '.join(query)

    # use elasticsearch search to find the best match for the query with the built in BM25 scoring.
    # it first searches the training datasets that were indexed previously
    res = es.search(index='train', q=query, df="question", _source=False, size=10)['hits']['hits']

    # find the best matching document by its ID
    matchedDocs = []
    
    for i in res:
        matchedDocs.append(es.get(id=i['_id'], index='train')['_source'])
   
    # set the category, type and score
    qCategory, qType, qScore = sortResults(matchedDocs, res, query)

    # if its a resource then we will try to find types in the abstracts index
    if qCategory == 'resource':
        qType = resourceTypes(query, qType, qScore)
    elif qCategory =='literal':
        if checkForTermSequence(query, 'when', 'is'):
            return 'literal', ['date'], qScore, ' '.join(query)

    return qCategory, qType, qScore, ' '.join(query)


def resourceTypes(query, tTypes, score):
    """Searches the abstracts index for the best matching types for a resource

    Takes a query, the types from the training data, and the score

    Returns a list of types
    """
    # search for the best match
    res = es.search(index='abstracts', q=query, df="description", _source=False, size=20)['hits']['hits']
    qTypes = []
    inserted = False
    # range through the results
    for i in res:
        # takes the type from the top result
        types = es.get(id=i['_id'], index='abstracts')['_source']['type']
        # if the training score is higher than the current score
        if i['_score'] < score and not inserted:
            # for each type
            for j in tTypes:
                # if the type is not already there
                if j not in qTypes:
                    # add it
                    qTypes.append(j)
            inserted = True
        # if the current score is less than a quarter of the query score
        elif i['_score'] < score/4 :
            # stop adding new types
            break
        # for each type in the types 
        for j in types:
            # if it is not already a type
            if j not in qTypes:
                # add the type
                qTypes.append(j)
    qTypes = dboResourceTypes(qTypes[:10])
    return qTypes


def dboResourceTypes(types):
    """Adds 'dbo:' to the start of the resource types
    
    Takes a list of types

    Returns a list of types with 'dbo:' at the start of each type
    """
    converted = []
    for i in types:
        # handle the case where the type might already be correctly formatted
        if 'dbo:' in i:
            converted.append(i)
        else:
            converted.append('dbo:' + i)
    return converted




##################
# New functions  #
##################
def sortResults(matchedDocs, res, query):
    """Takes the top result from each category (if it exists) and re-weighs the scoring

    Takes a list of the result documents from es.get, the result list from es.search, and the query

    returns the best category, type and score
    """
    # create an entry for each type of category with the document and the score
    optionsDict = {'resource':[[],-1.0],'literal':[[],-1.0],'boolean':[[],-1.0]}
    # for each document from the results list
    for i, j in enumerate(matchedDocs):
        # if the category is resource and the resource isn't already filled in
        if j['category'] == 'resource' and optionsDict['resource'][1]==-1.0:
            # add the type to the list and re-weigh the scoring based on the query
            optionsDict['resource'] = [j['type'], weightResourceScore(query, res[i]['_score'])]
        elif j['category'] == 'literal' and optionsDict['literal'][1]==-1.0:
            optionsDict['literal'] = [j['type'], weighLiteralScore(query, res[i]['_score'])]
        elif j['category'] == 'boolean' and optionsDict['boolean'][1]==-1.0:
            optionsDict['boolean'] = [j['type'], weighBooleanScore(query, res[i]['_score'])]
    
    bestCategory = 'resource'
    bestType = ['dbo:Thing']
    bestScore = -1.0

    for i, j in optionsDict.items():
        if j[1] > bestScore:
            bestCategory = i
            bestType = j[0]
            bestScore = j[1]

    return bestCategory, bestType, bestScore


# all of the score increases are based off of things established in ../analysis/
def weightResourceScore(query, score):
    """Changes resource weighing based on the first word
    
    Takes the query and the initial score

    Return the new score
    """
    if query[0] == 'is':
        score += 0.2
    elif query[0] == 'wa':
        score += 0.2
    elif query[0] == 'doe':
        score += 0.3
    elif query[0] == 'did':
        score += 0.5
    elif query[0] == 'are':
        score += 0.3
    elif query[0] == 'do':
        score += 0.8
    elif query[0] == 'were':
        score += 0.0
    elif query[0] == 'what':
        score += 7.1
    elif query[0] == 'ha':
        score += 2.0
    elif query[0] == 'can':
        score += 5.6
    elif query[0] == 'when':
        score += 1.0
    elif query[0] == 'which':
        score += 3.3
    elif query[0] == 'how':
        score += 0.9
    elif query[0] == 'in':
        score += 6.4
    elif query[0] == 'where':
        score += 9.2
    elif query[0] == 'give':
        score += 6.6
    elif query[0] == 'the':
        score += 6.9
    elif query[0] == 'name':
        score += 9.9
    elif query[0] == 'tell':
        score += 9.4
    elif query[0] == 'for':
        score += 9.1
    elif query[0] == 'list':
        score += 9.7
    return score

def weighLiteralScore(query, score):
    """Changes literal weighing based on the first word
    
    Takes the query and the initial score

    Return the new score
    """
    if query[0] == 'wa':
        score += 0.1
    elif query[0] == 'did':
        score += 0.1
    elif query[0] == 'are':
        score += 0.1
    elif query[0] == 'do':
        score += 0.3
    elif query[0] == 'what':
        score += 2.8
    elif query[0] == 'can':
        score += 1.2
    elif query[0] == 'when':
        score += 8.8
    elif query[0] == 'which':
        score += 3.3
    elif query[0] == 'how':
        score += 9.0
    elif query[0] == 'who':
        score += 0.4
    elif query[0] == 'in':
        score += 3.4
    elif query[0] == 'count':
        score += 10.0
    elif query[0] == 'where':
        score += 0.7
    elif query[0] == 'give':
        score += 3.3
    elif query[0] == 'the':
        score += 2.8
    elif query[0] == 'tell':
        score += 0.4
    elif query[0] == 'for':
        score += 0.8
    elif query[0] == 'list':
        score += 0.2
    return score

def weighBooleanScore(query, score):
    """Changes boolean weighing based on the first word
    
    Takes the query and the initial score

    Return the new score
    """
    if query[0] == 'is':
        score += 9.6
    elif query[0] == 'wa':
        score += 9.5
    elif query[0] == 'doe':
        score += 9.6
    elif query[0] == 'did':
        score += 9.3
    elif query[0] == 'are':
        score += 9.6
    elif query[0] == 'do':
        score += 8.7
    elif query[0] == 'were':
        score += 10.0
    elif query[0] == 'what':
        score += 7.1
    elif query[0] == 'ha':
        score += 7.8
    elif query[0] == 'can':
        score += 3.2
    elif query[0] == 'the':
        score += 0.2
    return score


def checkForTermSequence(query, term1, term2):
    """Checks the query if the terms given appear in order
    
    Takes the query and the two terms

    Returns a bool
    """
    # starts from the first index to avoid indexoutofbounds
    for i, j in enumerate(query[1:]):
        # i starts from 0 and j starts from 1 so this works
        if query[i] == term1 and j == term2:
            return True
    return False

