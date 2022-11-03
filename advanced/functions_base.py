import json
import re
import nltk


def preprocess(doc):
    """Preprocesses a document
    Taken from A2.1 assignment
    """
    ps = nltk.stem.PorterStemmer()
    return [ps.stem(term) for term in re.sub(r"[^\w]|_", " ", doc).lower().split()]


def loadData(filelocation):
    """Loads a json training dataset and returns it as a list of dictionaries.
    The keys are:

    'ID', 'question', 'category', 'type'
    """
    with open(filelocation, 'r', encoding='utf-8') as file:
        f = json.load(file)
        print('Successfully loaded ', filelocation)
        return f


def writeData(filelocation, dictionary):
    """Takes a filelocation and a dictionary and turns it into a json file
        have to make sure when making the dict that its the correct format.
    """
    # set the indent so that it looks pretty
    json_object = json.dumps(dictionary, indent=2)
    # open the file and write to it
    with open(filelocation, "w") as file:
        print('Writing to: ', filelocation)
        file.write(json_object)


def answerList(quesList, train, procNum , retDict):
    """Takes a list of questions, a list of the training dataset, the process number and the dictionary it will return
    and tries to classify the questions

    Returns a dictionary with the process id as key with the modified input list as value
    """
    num_questions = len(quesList)
    # ranges through the questions, we need the iterator to save answers to the list
    for i, j in enumerate(quesList):
        # answer the question
        category, type, score = answerQuery(j, train, procNum)
        # prints out the progress of question answering, taken from A2.1
        try:
            if (i + 1) % (num_questions // 100) == 0:
                print(f"{round(100*(i/num_questions))}% answered. in process {procNum}")
        except:
            # sometimes with a reduced dataset this will freak out and break so we need to catch those errors
            print('something went wrong with the progress printout in process', procNum)
        # add the category, type and score to the current question entry
        quesList[i]['category'] = category
        quesList[i]['type'] = type
        quesList[i]['score'] = score
    # return the dict with the process number as key
    retDict[procNum] = quesList
