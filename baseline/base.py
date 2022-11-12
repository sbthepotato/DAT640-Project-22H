from functions_base import *
import time
import datetime
import multiprocessing
import numpy


if __name__=="__main__":
    # start time of program
    start = time.time()
    print(datetime.datetime.now())

    # loads the questions into a list of dicts
    dbpedia_questions = loadData('../datasets/DBpedia/smarttask_dbpedia_test_questions.json')
    
    # creates a manager to return the values from the multiprocessing
    mana = multiprocessing.Manager()
    retDict = mana.dict()

    # splits the questions list into nr_cpu numpy.arrays
    split = numpy.array_split(dbpedia_questions, SPLITS)

    # creates a list of workers (processes)
    workers = []
    for i in range(SPLITS):
        # predicts category and type of question list based on training dataset and simple BM25 scoring
        #p = multiprocessing.Process(target=answerList, args=(split[i], train, i, retDict))
        p = multiprocessing.Process(target=answerList, args=(split[i], i, retDict))
        # add to the list of workers
        workers.append(p)
        # start the worker
        p.start()
    
    # wait for each worker to finish
    for p in workers:
        p.join()
    
    # sort the ret dict (in case of out of order finish)
    oRetDict = dict(sorted(retDict.items()))
    ansList = []
    # take the values from the dict and add them to an answer list
    for j in oRetDict.values():
        # the turn the numpy arrays back into a normal list
        ansList += j.tolist()

    # writes the list with answers into the same directory with the test and train files P
    writeData('../datasets/DBpedia/smarttask_dbpedia_test_answers_base.json', ansList)

    # runtime for fun
    end = time.time()
    print('This program took: ', datetime.timedelta(seconds=end-start), ' (h:mm:ss:ms) to run')
