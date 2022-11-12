from functions_indexing import *
import time
import datetime
import multiprocessing

import nltk
nltk.download('stopwords')


if __name__ =="__main__":
    # start time of program
    start = time.time()

    # load the abstracts into a list of strings
    #abstracts = loadDataTTF('../datasets/DBpedia/short_abstracts_en.ttl')
    abstracts = loadDataTTF('../datasets/DBpedia/long_abstracts_en.ttl')

    # split the abstracts, cant use the numpy one because Python just terminates due to lack of memory (lmao)
    split = list(splitFunc(abstracts, SPLITS_clean))
    # clear abstracts from memory
    del abstracts

    # create multiprocessing manager
    mana = multiprocessing.Manager()
    # dict for processes to return to
    retDict = mana.dict()
    # list of workers
    workers = []
    for i in range(SPLITS_clean):
        # process the abstracts
        p = multiprocessing.Process(target=processAbstracts, args=(split[0], i, retDict))
        # add to the list of workers
        workers.append(p)
        # start worker
        p.start()
        # clear from memory
        del split[0]
    del split
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
    