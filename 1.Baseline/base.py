from functions_base import *
import time
from datetime import timedelta
from multiprocessing import Process, Manager
import numpy as np

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
    mana = Manager()
    retDict = mana.dict()

    # splits the questions into an array
    split = np.array_split(dbpedia_questions, 4)
    # creates a list of workers (processes)
    workers = []
    for i in range(4):
        # predicts category and type of question list based on training dataset and simple BM25 scoring
        p = Process(target=answerList, args=(split[i], dbpedia_train, i, retDict))
        # add to the list of workers
        workers.append(p)
        # start the worker
        p.start()
    # wait for each worker to finish
    for proc in workers:
        proc.join()
    
    ansList = []
    # order the dict based on the process key, shouldn't be necessary but nice to have
    oRetDict = dict(sorted(retDict.items()))
    # take the values from the dict and add them to an answer list
    for j in oRetDict.values():
        # the turn the numpy arrays back into a normal list
        ansList += j.tolist()

    # writes the list with answers into the same directory with the test and train files
    writeData('../datasets/DBpedia/smarttask_dbpedia_test_answers.json', ansList)
    # runtime for fun
    end = time.time()
    print('This program took: ', timedelta(seconds=end-start), ' (h:mm:ss) to run')
