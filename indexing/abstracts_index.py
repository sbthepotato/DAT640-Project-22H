from functions_indexing import *
from elasticsearch import Elasticsearch
import time
import datetime
import multiprocessing

# name of the index
INDEX_NAME = 'abstracts_short'

# settings for how it should look like
INDEX_SETTINGS = {
    "mappings": {
        "properties": {
            "description": {
                "type": "text", 
                "term_vector": "yes", 
                "analyzer": "english"
            }
        }
    }
}

# defines as a global variable for the multiprocessing
es = Elasticsearch(maxsize=MAX_CONNECTS, timeout=30, max_retries=10, retry_on_timeout=True)

# has to be in this file due to the elasticsearch instance
def elastic_index(doc, procNum):
    length = len(doc)
    for i, j in enumerate(doc):
        progressPrint(i, length, procNum)
        es.index(index=INDEX_NAME, id=j['id'], document=j)


if __name__=="__main__":
    start = time.time()
    print(datetime.datetime.now())

    # make sure the elasticsearch is running
    es.info()

    # reset the index since we're making a new one
    reset_index(es, INDEX_NAME, INDEX_SETTINGS)

    # load the abstracts
    abstracts = loadDataJSON('../datasets/DBpedia/dbpedia_abstracts_short.json')
    # split them into SPLITS new lists
    split = list(splitFunc(abstracts, SPLITS))
    # clear from memory
    del abstracts

    # creates a list of workers (processes)
    workers = []
    for i in range(SPLITS):
        # indexes the abstracts
        p = multiprocessing.Process(target=elastic_index, args=(split[i], i, ))
        # add to the list of workers
        workers.append(p)
        # start the worker
        p.start()
    del split
    # wait for each worker to finish
    for p in workers:
        p.join()
  
    # runtime for fun
    end = time.time()
    print('This program took: ', datetime.timedelta(seconds=end-start), ' (h:mm:ss:ms) to run')
