from functions_index import *
import os
import time
import datetime
import multiprocessing
import numpy


if __name__ =="__main__":
    # start time of program
    start = time.time
    
    # load the instance types into a list of lists
    instaceTypes = loadDataTurtle('../datasets/DBpedia/instance_types_en.ttl')
    # load the questions into a list of dicts
    dbpedia_questions = loadDatajson('../datasets/DBpedia/smarttask_dbpedia_test_questions.json')
    # preprocess the questions
    for i, j in enumerate(dbpedia_questions):
        dbpedia_questions[i]['question'] = preprocess(str(j['question']))

    # creates a manager to return the values from the multiprocessing
    mana = multiprocessing.Manager()
    retDict = mana.dict()

    #counts the cpu cores to decide how many processes to create
    nr_cpu = os.cpu_count()
    print(nr_cpu, ' cpu cores detected')

    # splits the instance types list into nr_cpu numpy.arrays
    split = numpy.array_split(instaceTypes, nr_cpu)
    print('successfully split the instance types into ', len(split), ' pieces.')

    # creates a list of workers (processes)
    workers = []
    for i in range(nr_cpu):
        # predicts category and type of question list based on training dataset and simple BM25 scoring
        p = multiprocessing.Process(target=checkmatch, args=(split[i], dbpedia_questions, i, retDict))
        # add to the list of workers
        workers.append(p)
        # start the worker
        p.start()
    # wait for each worker to finish
    for p in workers:
        p.join()


    ansList = []
    for j in retDict.values():
        ansList += j.tolist()

    # writes the cleaned list into the same directory with all the other DBpedia stuff
    writeDataTSV('../datasets/DBpedia/instance_types_en_clean.tsv')

    # runtime for fun
    end = time.time()
    print('This program took: ', datetime.timedelta(seconds=end-start), ' (h:mm:ss:ms) to run')