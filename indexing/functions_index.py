import json
import re
import nltk



def loadDataTTF(filelocation):
    """Loads a ttf file and returns it as a list with each line being a new element
    """
    with open(filelocation, 'r', encoding='utf-8') as file:
        list_file = []
        for line in file:
            list_file.append(line)
        print('loaded ', filelocation)
        return list_file


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
        # clean the ud and the type of the uri
        id = ' '.join(cleanUri(id))
        #print(id)
        idtype = cleanUri(urls[2])
        # if the id isnt the same as the last one
        if id != previd:
            # then append the last one
            retlist.append(currentDict)
            # clear the dict
            currentDict = {'id': '', 'type': []}
            # set the new id
            previd = id
            currentDict['id'] = id
            currentDict['type'].append(idtype)
        else:
            # if it is the same then add it but only if that type doesnt already exist.
            if idtype not in currentDict['type']:
                currentDict['type'].append(idtype)
    print('cpu ', procNum, ' finished processing instance types')
    # don't return the first element cause its empty
    retDict[procNum] = retlist[1:]


def processAbstracts(file_list, procNum, retDict):
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
        url = ' '.join(cleanUri(url[0]))
        # find the description
        desc = re.findall(regDesc, line)
        # preprocess and join it back together
        desc = ' '.join(preprocess(str(desc)))
        # put it in a dict and add the dict to the return list
        currentDict= {'id':url, 'description':desc}
        retlist.append(currentDict)
    print('cpu ', procNum, ' finished processing abstracts')
    retDict[procNum] = retlist


def matchDescToType(descList, typeList, procNum, retDict):
    """Compares the ID of the typelist and the abstracts list to match the entries,

    returns a dict with a list of dicts with the id, types and description
    """
    matchedList = []
    desc_len = len(descList)
    for i, j in enumerate(descList):
        for k, m in enumerate(typeList):
            if m['id'] == j[0]:
                m['description'] = j[1]
                del typeList[k]
        try:
            if (i + 1) % (desc_len // 100) == 0:
                print(f"{round(100*(i/desc_len))}% matched. in process {procNum}")
        except:
            # sometimes with a reduced dataset this will freak out and break so we need to catch those errors
            print('something went wrong with the progress printout in process', procNum)

        matchedList.append(m)
        
    retDict[procNum] = matchedList


def cleanUri(uri):
    """Cleans a uri and returns a cleaned version
    Adapted from A3.1
    """
    return preprocess(uri.split("/")[-1].replace("_", " ").replace('>', ''))


def preprocess(doc):
    """Preprocesses a document
    Taken from A2.1 assignment
    """
    ps = nltk.stem.PorterStemmer()
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
