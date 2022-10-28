from functions_base import preprocess
import math
import rank_bm25


def answerList(quesList, train, procNum , retDict):
    """Takes a list of questions, a list of the training dataset, the process number and the dictionary it will return
    and tries to classify the questions

    Returns a dictionary with the process id as key with the modified input list as value
    """
    num_questions = len(quesList)
    # ranges through the questions, we need the iterator to save answers to the list
    for i, j in enumerate(quesList):
        # answer the question
        category, type, score = answerQuery(j, train, procNum)
        # prints out the progress of question answering, taken from A2.1
        try:
            if (i + 1) % (num_questions // 100) == 0:
                print(f"{round(100*(i/num_questions))}% answered. in process {procNum}")
        except:
            # sometimes with a reduced dataset this will freak out and break so we need to catch those errors
            print('something went wrong with the progress printout in process', procNum)
        # add the category, type and score to the current question entry
        quesList[i]['category'] = category
        quesList[i]['type'] = type
        quesList[i]['score'] = score
    # return the dict with the process number as key
    retDict[procNum] = quesList


def answerQuery(query, train, procNum):
    """Takes a question and the training dataset and finds the highest score match from the training dataset

    Returns the category, type and score of a question
    """
    queryP = preprocess(str(query['question']))
    
    # catch zerodivision errors to avoid termination
    try:
        bm25 = rank_bm25.BM25Okapi(queryP)
    except ZeroDivisionError as e:
        print('Zero division while creating instance in process ', procNum)
        print('Question id: ', query['id'])
        print(e)
        # we'll just use a default category, type and score
        return 'boolean', 'boolean', -1.0
    # score the query against the dataset
    answers = scoreQuery(bm25, train)
    # go through the possible classifications and return the best one
    return classifyQuery(answers)


def scoreQuery(bm25, train):
    """Takes the bm25 class and the training dataset and finds the highest score match from each category

    Returns a dict of dicts for each category (resource, literal, boolean)
    """
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
    """Takes the current query from the training dataset, the score it got and the options dict and updates the option dict
    
    Returns the updated optionsDict (same one as given as input)
    """
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
    """Doesnt do anything special yet but will:
    takes the optionsDict with the highest performing answers for each category and modifies the scores to try to improve the match

    Returns the highest score category, types and its score
    """
    # TODO: This whole thing
    scoreA = -1.0
    categoryA = 'boolean'
    typeA = 'boolean'

    for i, j in answers.items():
        if j['score'] > scoreA:
            categoryA = i
            typeA = j['type']
    return categoryA, typeA, scoreA
    
