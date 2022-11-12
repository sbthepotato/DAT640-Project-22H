from functions_indexing import *

from abstracts_index import INDEX_NAME


###################################################
# THIS FILE IS USED FOR TEMPORARY EXPERIMENTATION #
#                  IGNORE IT                      #
###################################################


if __name__=="__main__":

    ques = 'How many ingredients are in the grain} ?'

    query = preprocess(ques)

    res = es.search(index=INDEX_NAME, q=query, df="description", _source=False, size=50)['hits']['hits']
    print(res)
    print(res[0]['_id'])
    print(res[0]['_score'])


    #test = es.get(id=res[0]['_id'], index=INDEX_NAME)['_source']

    """  try:
        test = es.get(id='Anarchism', index=INDEX_NAME)['_source']
        print(test)
        #print(test)
    except Exception as e:
        ...
        print('test2')
        #print('exception: ', e)
    """

    types = []
    for i in range(20):
        qtype = (es.get(id=res[i]['_id'], index=INDEX_NAME)['_source']['type'])
        for j in qtype:
            if j not in types and len(types) < 6:
                types.append(j)

    print(types)


    print('test')

    print(es.count(index='abstracts')['count'])
    