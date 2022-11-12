from functions_indexing import *
import time
import datetime
import multiprocessing

# name of the index
INDEX_NAME = 'train'

# settings for how it should look like
INDEX_SETTINGS = {
    "mappings": {
        "properties": {
            "question": {
                "type": "text", 
                "term_vector": "yes", 
                "analyzer": "english"
            },
            "category": {
                "type": "text", 
                "term_vector": "no", 
                "analyzer": "keyword"
            },
            "type": {
                "type": "text", 
                "term_vector": "no", 
                "analyzer": "keyword"
            },
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

    # load the training datasets
    dbpedia_train = loadDataJSON('../datasets/DBpedia/smarttask_dbpedia_train.json')
    wikidata_train = loadDataJSON('../datasets/Wikidata/lcquad2_anstype_wikidata_train.json')
    # combine the lists
    train = dbpedia_train + wikidata_train
    del dbpedia_train
    del wikidata_train

    for i, j in enumerate(train):
        train[i]['question'] = ' '.join(preprocessBasic(str(j['question'])))


    # split them into SPLITS new lists
    split = list(splitFunc(train, SPLITS))
    # clear from memory
    del train

    # creates a list of workers (processes)
    workers = []
    for i in range(SPLITS):
        # indexes the training datasets
        p = multiprocessing.Process(target=elastic_index, args=(split[i], INDEX_NAME, i, ))
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
