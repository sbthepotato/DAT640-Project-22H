from functions_index import *


if __name__=="__main__":
    abstracts = loadDataJSON('../datasets/DBpedia/dbpedia_abstracts_short.json')

    print(len(abstracts))

    questions = loadDataJSON('../datasets/DBpedia/smarttask_dbpedia_test_questions.json')

    for i, j in enumerate(questions):
        questions[i]['question'] = preprocess(j['question'])

    

    newAbstracts = []
    abstracts = abstracts
    length = len(abstracts)

    for idx, i in enumerate(abstracts):
        progressPrint(idx, length, 0)
        found = False
        for j in questions:
            if not found:
                for word in j['question']:
                    if word in i['description']:
                        newAbstracts.append(i)
                        found = True
                        break
                    

    print(len(newAbstracts))
