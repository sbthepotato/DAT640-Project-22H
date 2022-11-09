from functions_index import *
import os
import time
import datetime
import numpy
import multiprocessing


if __name__ =="__main__":
    # start time of program
    start = time.time()

    # counts cpu cores and divides by 2 to decide how many processes to make
    nr_cpu = round(os.cpu_count()/2)

    # load the instance types into a list of dicts
    instanceTypes = loadDataTTF('../datasets/DBpedia/instance_types_en.ttl')
    # split the instance types
    split = numpy.array_split(instanceTypes, nr_cpu)
    # clear instancetypes from memory
    del instanceTypes
    # create multiprocessing manager
    mana = multiprocessing.Manager()
    # dict for processes to return to
    retDict = mana.dict()
    # list of workers
    workers = []
    # for each cpu
    for i in range(nr_cpu):
        # process the instance types
        p = multiprocessing.Process(target=processInstanceTypes, args=(split[i].tolist(), i, retDict))
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

    # write the instance types to a json file
    writeDataJSON('../datasets/DBpedia/dbpedia_instance_types.json', processedList)

    # runtime for fun
    end = time.time()
    print('This program took: ', datetime.timedelta(seconds=end-start), ' (h:mm:ss:ms) to run')