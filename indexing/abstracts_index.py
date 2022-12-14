from functions_indexing import *
import time
import datetime
import multiprocessing

# name of the index, change which one is commented if you want to change which one to index
INDEX_NAME = 'abstracts'

# settings for how it should look like
INDEX_SETTINGS = {
    "mappings": {
        "properties": {
            "description": {
                "type": "text", 
                "term_vector": "yes", 
                "analyzer": "english"
            },
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

    # make sure the elasticsearch is running
    es.info()

    # reset the index since we're making a new one
    reset_index(es, INDEX_NAME, INDEX_SETTINGS)

    # load the abstracts, change which one is commented if you want to change which one to index
    abstracts = loadDataJSON('../datasets/DBpedia/dbpedia_abstracts.json')

    # split them into SPLITS new lists
    split = list(splitFunc(abstracts, SPLITS_index))
    # clear from memory
    del abstracts

    # creates a list of workers (processes)
    workers = []
    for i in range(SPLITS_index):
        # indexes the abstracts
        p = multiprocessing.Process(target=elastic_index_abstracts, args=(split[0], INDEX_NAME, i, ))
        # add to the list of workers
        workers.append(p)
        # start the worker
        p.start()
        del split[0]
    del split
    # wait for each worker to finish
    for p in workers:
        p.join()
  
    # runtime for fun
    end = time.time()
    print('This program took: ', datetime.timedelta(seconds=end-start), ' (h:mm:ss:ms) to run')
