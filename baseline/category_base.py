from functions_base import *
import os
import time
import datetime
import multiprocessing
import numpy


if __name__=="__main__":
    # start time of program
    start = time.time()
    # loads the dbpedia and wikidata training dataset into a list of dicts
    dbpedia_train = loadData('../datasets/DBpedia/smarttask_dbpedia_train.json')
    wikidata_train = loadData('../datasets/Wikidata/lcquad2_anstype_wikidata_train.json')
    # combine the lists
    train = dbpedia_train + wikidata_train

    # preprocess the training list questions
    for i, j in enumerate(train):
        train[i]['question'] = preprocess(str(j['question']))

    # loads the questions into a list of dicts
    dbpedia_questions = loadData('../datasets/DBpedia/smarttask_dbpedia_test_questions.json')
    
    # creates a manager to return the values from the multiprocessing
    mana = multiprocessing.Manager()
    retDict = mana.dict()

    # counts the cpu cores to decide how many processes to create
    nr_cpu = min(os.cpu_count(), 16)
    print(nr_cpu, ' cpu cores detected')

    # splits the questions list into nr_cpu numpy.arrays
    split = numpy.array_split(dbpedia_questions, nr_cpu)
    print('successfully split the questions into ', len(split), ' pieces.')

    # creates a list of workers (processes)
    workers = []
    for i in range(nr_cpu):
        # predicts category and type of question list based on training dataset and simple BM25 scoring
        p = multiprocessing.Process(target=answerList, args=(split[i], train, i, retDict))
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
