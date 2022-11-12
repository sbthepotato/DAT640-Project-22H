from functions_indexing import *
from elasticsearch import Elasticsearch
import time
import datetime
import multiprocessing

# name of the index
INDEX_NAME = 'instances'

# settings for how it should look like
INDEX_SETTINGS = {
    "mappings": {
        "properties": {
            "type": {
                "type": "text", 
                "term_vector": "yes", 
                "analyzer": "keyword"
            }
        }
    }
}


if __name__=="__main__":
    start = time.time()
    print(datetime.datetime.now())

    # make sure elasticsearch is running
    es.info()

    # reset the index since we're making a new one
    reset_index(es, INDEX_NAME, INDEX_SETTINGS)

    # load the instances
    instances = loadDataJSON('../datasets/DBpedia/dbpedia_instance_types.json')
    # split the instances into SPLITS new lists
    split = list(splitFunc(instances, SPLITS_index))
    # clear instances from memory
    del instances

    # creates a list of workers (processes)
    workers = []
    for i in range(SPLITS_index):
        # indexes the instances
        p = multiprocessing.Process(target=elastic_index, args=(split[0], INDEX_NAME, i, ))
        # add to the list of workers
        workers.append(p)
        # start the worker
        p.start()
        # clear from memory
        del split[0]
    del split
    # wait for each worker to finish
    for p in workers:
        p.join()
  
    # runtime for fun
    end = time.time()
    print('This program took: ', datetime.timedelta(seconds=end-start), ' (h:mm:ss:ms) to run')
