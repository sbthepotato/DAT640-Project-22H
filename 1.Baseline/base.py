import base_functions as fun


if __name__=="__main__":
    # loads the training dataset into a dict
    dbpedia_train = fun.loadData('../datasets/DBpedia/smarttask_dbpedia_train.json')
    # loads the questions into a dict
    dbpedia_questions = fun.loadData('../datasets/DBpedia/smarttask_dbpedia_test_questions.json')
    # writes the dict with answers into the same directory with the test and train files
    fun.writeData('../datasets/DBpedia/smarttask_dbpedia_test_answers.json', dbpedia_questions)

