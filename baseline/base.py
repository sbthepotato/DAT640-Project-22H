from functions_base import *
import time
from datetime import timedelta
import multiprocessing
import numpy as np
import os

if __name__=="__main__":
    # start time of program
    start = time.time()
    # loads the dbpedia training dataset into a list of dicts
    dbpedia_train = loadData('../datasets/DBpedia/smarttask_dbpedia_train.json')

    # loads the questions into a list of dicts
    dbpedia_questions = loadData('../datasets/DBpedia/smarttask_dbpedia_test_questions.json')
    # preprocess the training list questions
    for i in dbpedia_train:
        i['question'] = preprocess(str(i['question']))
    
    # creates a manager to return the values from the multiprocessing
    mana = multiprocessing.Manager()
    retDict = mana.dict()

    # counts the cpu cores to decide how many processes to create
    nr_cpu = os.cpu_count()
    print(nr_cpu, ' cpu cores detected')

    # splits the questions list into nr_cpu np.arrays
    split = np.array_split(dbpedia_questions, nr_cpu)
    print('Split the questions into ', len(split), ' pieces.')

    # creates a list of workers (processes)
    workers = []
    for i in range(nr_cpu):
        # predicts category and type of question list based on training dataset and simple BM25 scoring
        p = multiprocessing.Process(target=answerList, args=(split[i], dbpedia_train, i, retDict))
        # add to the list of workers
        workers.append(p)
        # start the worker
        p.start()
    # wait for each worker to finish
    for p in workers:
        p.join()
    
    ansList = []
    # order the dict based on the process key, shouldn't be necessary but nice to have
    oRetDict = dict(sorted(retDict.items()))
    # take the values from the dict and add them to an answer list
    for j in oRetDict.values():
        # the turn the numpy arrays back into a normal list
        ansList += j.tolist()

    # writes the list with answers into the same directory with the test and train files P
    writeData('../datasets/DBpedia/smarttask_dbpedia_test_answers_base.json', ansList)
    # runtime for fun
    end = time.time()
    print('This program took: ', timedelta(seconds=end-start), ' (h:mm:ss:ms) to run')
