from functions_index import *
import os
import time
import datetime
import multiprocessing
import numpy


if __name__ =="__main__":
    # start time of program
    start = time.time()

    #counts the cpu cores to decide how many processes to create
    nr_cpu = os.cpu_count()
    half_cpu = round(nr_cpu/2)
    print(nr_cpu, ' cpu cores detected')

    # load the instance types into a list of dicts
    instanceTypes = loadDataTTF('../datasets/DBpedia/instance_types_en.ttl')
    # process the instance types (multiprocessed)
    instanceTypes = processInstanceTypesMP(instanceTypes, half_cpu)

    # load the abstracts into a list of lists 
    abstracts = loadDataTTF('../datasets/DBpedia/short_abstracts_en.ttl')
    abstracts = processAbstractsMP(abstracts, half_cpu)
    

    print('nr instance types: ', len(instanceTypes))
    print('nr abstracts: ', len(abstracts))



    """ # creates a manager to return the values from the multiprocessing
    mana = multiprocessing.Manager()
    retDict = mana.dict()

    # creates a list of workers (processes)
    workers = []
    for i in range(nr_cpu):
        # predicts category and type of question list based on training dataset and simple BM25 scoring
        p = multiprocessing.Process(target=matchDescToType, args=(split[i], instaceTypes, i, retDict))
        # add to the list of workers
        workers.append(p)
        # start the worker
        p.start()
    # wait for each worker to finish
    for p in workers:
        p.join()


    # order the dict based on the process key, shouldn't be necessary but nice to have
    oRetDict = dict(sorted(retDict.items()))
    # take the values from the dict and add them to an answer list
    typeDescList = []
    for j in oRetDict.values():
        # the turn the numpy arrays back into a normal list
        typeDescList += j.tolist()

    # writes the cleaned list into the same directory with all the other DBpedia stuff
    # writeDataTSV('../datasets/DBpedia/instance_types_en_clean.tsv')
    

    writeDataJSON('../datasets/DBpedia/dbpedia_type_descriptions.json', typeDescList) """

    # runtime for fun
    end = time.time()
    print('This program took: ', datetime.timedelta(seconds=end-start), ' (h:mm:ss:ms) to run')