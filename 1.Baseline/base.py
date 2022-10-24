import base_functions as fun

if __name__=="__main__":
    # loads the training dataset into a dict
    dbpedia_train = fun.loadData('../datasets/DBpedia/smarttask_dbpedia_train.json')
    # loads the questions into a dict
    dbpedia_questions = fun.loadData('../datasets/DBpedia/smarttask_dbpedia_test_questions.json')
    
    for i in dbpedia_train:
        i['question'] = fun.preprocess(str(i['question']))
    print('finished preprocess train')

    for i in dbpedia_questions:
        i['question'] = fun.preprocess(str(i['question']))
    print('finished preprocess questions')

    num_questions = len(dbpedia_questions)
    for i, j in enumerate(dbpedia_questions):
        category, type = fun.answerQuery(j['question'], dbpedia_train)
        if (i + 1) % (num_questions // 100) == 0:
            print(f"{round(100*(i/num_questions))}% answered.")

    # writes the dict with answers into the same directory with the test and train files
    fun.writeData('../datasets/DBpedia/smarttask_dbpedia_test_answers.json', dbpedia_questions)

