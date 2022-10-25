from functions_base import *
import time
from datetime import timedelta

if __name__=="__main__":
    # start time of program
    start = time.time()
    # loads the dbpedia training dataset into a list of dicts
    dbpedia_train = loadData('../datasets/DBpedia/smarttask_dbpedia_train.json')
    # loads the wikidata training dataset into a list of dicts
    wikidata_train = loadData('../datasets/Wikidata/lcquad2_anstype_wikidata_train.json')
    # adds the training lists together
    train = dbpedia_train + wikidata_train
    # loads the questions into a list of dicts
    dbpedia_questions = loadData('../datasets/DBpedia/smarttask_dbpedia_test_questions.json')
    # preprocess the training list questions
    for i in train:
        i['question'] = preprocess(str(i['question']))
    # predicts category and type of question list based on training dataset and simple BM25 scoring
    dbpedia_questions = answerList(dbpedia_questions, train)
    # writes the dict with answers into the same directory with the test and train files
    writeData('../datasets/DBpedia/smarttask_dbpedia_test_answers.json', dbpedia_questions)
    # runtime for fun
    end = time.time()
    print('This program took: ', timedelta(seconds=start-end), ' to run')
