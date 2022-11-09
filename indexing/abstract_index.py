from functions_index import *
import os
import time
import datetime
import multiprocessing


if __name__ =="__main__":
    # start time of program
    start = time.time()

    # counts cpu cores and divides by 2 to decide how many processes to make
    #nr_cpu = round(os.cpu_count()/2)

    # load the abstracts into a list of dicts
    abstracts = loadDataTTF('../datasets/DBpedia/long_abstracts_en.ttl')
    # split the instance types, cant use the numpy one because Python just terminates due to lack of memory (lmao)
    split = list(splitFunc(abstracts, 4))
    # clear abstracts from memory
    del abstracts
    # create multiprocessing manager
    mana = multiprocessing.Manager()
    # dict for processes to return to
    retDict = mana.dict()
    # list of workers
    workers = []
    # for each cpu
    for i in range(4):
        # process the abstracts
        p = multiprocessing.Process(target=processAbstracts, args=(split[i], i, retDict))
        # add to the list of workers
        workers.append(p)
        # start worker
        p.start()
    # wait for workers to finish
    for p in workers:
        p.join()
    # sort the ret dict (in case of out of order finish)
    sortedRetDict = dict(sorted(retDict.items()))
    processedList = []
    for j in sortedRetDict.values():
        processedList += j 

    # write the abstracts to a json file
    writeDataJSON('../datasets/DBpedia/dbpedia_abstracts.json', processedList)

    # runtime for fun
    end = time.time()
    print('This program took: ', datetime.timedelta(seconds=end-start), ' (h:mm:ss:ms) to run')