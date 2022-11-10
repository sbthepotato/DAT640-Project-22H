import json
import re
import pickle

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


def loadDataTTF(filelocation):
    """Loads a ttf file and returns it as a list with each line being a new element
    """
    with open(filelocation, 'r', encoding='utf-8') as file:
        list_file = []
        for line in file:
            list_file.append(line)
        print('Successfully loaded ', filelocation)
        return list_file


def loadDataJSON(filelocation):
    """Loads a json training dataset and returns it as a list of dictionaries.
    
    The keys for the instance_types are `id` and `type`

    The keys for abstracts are `id` and `description`
    """
    with open(filelocation, 'r', encoding='utf-8') as file:
        f = json.load(file)
        print('Successfully loaded ', filelocation)
        return f


def progressPrint(index, length, procnum):
    """Prints the current progress of processing something for a given process
    """
    try:
        if (index + 1) % (length // 100) == 0:
            print(f"{round(100*(index/length))}% processed. in process {procnum}")
    except:
        print('something went wrong with the progress printout in process', procnum)


def splitFunc(a, n):
    """splits list 'a' into 'n' pieces

    returns a Generator which needs to be converted back to a list

    from: https://stackoverflow.com/a/2135920
    """
    if n == 1:
        return a
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))


def processInstanceTypes(file_list, procNum, retDict):
    """Processes the instance types, takes an unprocessed list as input where each element is a line from the file.
    also takes the process number and the return dictionary for multiprocessing

    returns a dict with a list of the processed instance types
    """
    # regex to find stuff inside the urls
    regURL = "<(.*?)>"
    # create empty-ish dic
    currentDict = {'id': '', 'type': []}
    # previous id so that instances with multiple types get them all in the same place
    previd = ''
    # list with all return values
    retlist = []
    length = len(file_list)
    for i, line in enumerate(file_list):
        progressPrint(i, length, procNum)
        # skip the first and last line
        if line[0] == '#':
            continue
        # find the 3 urls
        urls = re.findall(regURL, line)
        # take the id and remove the number at the end
        id = re.sub(r'__\d', '', urls[0])
        # clean the id and the type of the uri
        id = ''.join(cleanUri(id))
        # split based on # because that means its multiple in one
        idtype = cleanUri(urls[2]).split('#') 
        # if the id isnt the same as the last one
        if id != previd:
            # then append the last one
            retlist.append(currentDict)
            # clear the dict
            currentDict = {'id': '', 'type': []}
            # set the new id
            previd = id
            currentDict['id'] = id
            for j in idtype:
                currentDict['type'].append(j)
        else:
            # if it is the same then add it but only if that type doesnt already exist.
            for j in idtype:
                if j not in currentDict['type']:
                    currentDict['type'].append(j)
    print('cpu ', procNum, ' finished processing instance types')
    # don't return the first element cause its empty
    retDict[procNum] = retlist[1:]


def processAbstracts(file_list, questions, procNum, retDict):
    # regex to find stuff inside the urls
    regURL = "<(.*?)>"
    regDesc = ' "(.*?)"@en .'
    # return list
    retlist = []
    length = len(file_list)
    for i, line in enumerate(file_list):
        progressPrint(i, length, procNum)
        # skip the first and last line
        if line[0] == '#':
            continue
        # find all the urls
        url = re.findall(regURL, line)
        # we only want the first one, clean it and join it
        url = ''.join(cleanUri(url[0]))
        # find the description
        desc = re.findall(regDesc, line)
        # preprocess and join it back together
        desc = preprocess(str(desc))
        # put it in a dict and add the dict to the return list
        found = False
        for j in questions:
            if not found:
                for word in j['question']:
                    if len(word) > 4:
                        if word in desc:
                            currentDict= {'id':url, 'description': ' '.join(desc)}
                            retlist.append(currentDict)
                            found = True
                            break
            else:
                break
    print('cpu ', procNum, ' finished processing abstracts')
    retDict[procNum] = retlist


def cleanUri(uri):
    """Cleans a uri and returns a cleaned version
    Taken from A3.1 assignment
    """
    return uri.split("/")[-1]


def preprocess(doc):
    """Preprocesses a document
    Taken from A3.1 assignment
    """
    # lowercase
    doc = doc.lower()
    # remove pattern
    pattern = r'[^\w]|_", " '
    doc = re.sub(pattern, ' ',doc)
    # tokenize
    doc = word_tokenize(doc)
    # stopword removal
    sw =  set(stopwords.words('english'))
    doc = [word for word in doc if not word in sw]
    # stemmer
    ps = PorterStemmer()
    doc = [ps.stem(word) for word in doc]
    return doc


def preprocessBasic(doc):
    """Preprocesses a document
    Taken from A2.1 assignment
    """
    ps = PorterStemmer()
    return [ps.stem(term) for term in re.sub(r"[^\w]|_", " ", doc).lower().split()]


def writeDataJSON(filelocation, dictionary):
    """Takes a filelocation and a dictionary and turns it into a json file
        have to make sure when making the dict that its the correct format.
    """
    # set the indent so that it looks pretty
    json_object = json.dumps(dictionary, indent=2)
    # open the file and write to it
    with open(filelocation, "w") as file:
        print('Writing to: ', filelocation)
        file.write(json_object)


def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        print('Writing to: ', filename)
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)
