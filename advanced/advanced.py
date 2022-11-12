from functions_base import *
from functions_advanced import *
import os
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

    # how many multiprocessing processes to make
    nr_splits = min(os.cpu_count(), 8)


    # splits the questions list into nr_splits numpy.arrays
    split = numpy.array_split(dbpedia_questions, nr_splits)
    # clear from memory
    del dbpedia_questions
   
    # creates a list of workers (processes)
    workers = []
    for i in range(nr_splits):
        # predicts category and type of question list based on training dataset and simple BM25 scoring
        p = multiprocessing.Process(target=answerList, args=(split[i].tolist(), i, retDict))
        # add to the list of workers
        workers.append(p)
        # start the worker
        p.start()
    # clear from memory
    del split

    # wait for each worker to finish
    for p in workers:
        p.join()
    
    # sort the ret dict (in case of out of order finish)
    oRetDict = dict(sorted(retDict.items()))
    # take the values from the dict and add them to an answer list
    ansList = []
    for j in oRetDict.values():
        ansList += j

    # writes the list with answers into the same directory with the test and train files P
    writeData('../datasets/DBpedia/smarttask_dbpedia_test_answers_advanced.json', ansList)
    
    # runtime for fun
    end = time.time()
    print('This program took: ', datetime.timedelta(seconds=end-start), ' (h:mm:ss:ms) to run')
