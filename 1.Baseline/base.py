import base_functions as fun
import sys
import subprocess

if __name__=="__main__":
    # prevents macs from sleeping, hopefully wont affect windows systems ?
    if 'darwin' in sys.platform:
        print('Running \'caffeinate\' on MacOSX to prevent the system from sleeping')
        subprocess.Popen('caffeinate')
    # loads the training dataset into a dict
    dbpedia_train = fun.loadData('../datasets/DBpedia/smarttask_dbpedia_train.json')
    # loads the questions into a dict
    dbpedia_questions = fun.loadData('../datasets/DBpedia/smarttask_dbpedia_test_questions.json')
    
    for i in dbpedia_train:
        i['question'] = fun.preprocess(str(i['question']))
    print('finished preprocess train')

    num_questions = len(dbpedia_questions)
    # quickly comment one or the other in/out to test program on reduced dataset
    #for i, j in enumerate(dbpedia_questions[:10]):
    for i, j in enumerate(dbpedia_questions):
        question_processed = fun.preprocess(str(j['question']))
        category, type = fun.answerQuery(question_processed, dbpedia_train)
        # prints out the progress of question answering, taken from A2.1
        try:
            if (i + 1) % (num_questions // 100) == 0:
                print(f"{round(100*(i/num_questions))}% answered.")
        except:
            print('something went wrong with the progress printout')
        dbpedia_questions[i]['category'] = category
        dbpedia_questions[i]['type'] = type

    print('finished answering dataset')
    # writes the dict with answers into the same directory with the test and train files
    fun.writeData('../datasets/DBpedia/smarttask_dbpedia_test_answers.json', dbpedia_questions)

