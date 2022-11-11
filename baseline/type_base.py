from functions_base import *
import time
import datetime


if __name__=="__main__":
    # start time of the program
    start = time.time()
    print(datetime.datetime.now())

    bm25 = openPickle('../datasets/DBpedia/bm25_abstracts.pkl')
    print('loaded the bm25 object')

    # loads the previously categorised dbpedia dataset into a list of dicts
    dbpedia_questions = loadData('../datasets/DBpedia/smarttask_dbpedia_test_answers_base.json')

    ansList = findTypeIDList(dbpedia_questions, bm25)

    """ abstracts = loadData('../datasets/DBpedia/dbpedia_abstracts_short.json')

    abstractsID = []
    for i in abstracts:
        abstractsID.append(i['id'])
    del abstracts """

    # writes the list with answers into the same directory with the test and train files P
    writeData('../datasets/DBpedia/smarttask_dbpedia_test_answers_base_short.json', ansList)
    # runtime for fun
    end = time.time()
    print('This program took: ', datetime.timedelta(seconds=end-start), ' (h:mm:ss:ms) to run')
