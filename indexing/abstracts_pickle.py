from functions_index import *
import rank_bm25

if __name__=="__main__":
    # load the abstracts
    abstracts = loadDataJSON('../datasets/DBpedia/dbpedia_abstracts_short.json')

    # create list of the descriptions
    abstractsDesc = []
    # load all the descriptions onto the list
    for i in abstracts:
        abstractsDesc.append(i['description'].split(' '))
    print('finished making abstract list')
    del abstracts

    bm25 = rank_bm25.BM25Okapi(abstractsDesc)
    print('finished creating bm25 object')
    del abstractsDesc

    save_object(bm25, '../datasets/DBpedia/bm25_abstracts.pkl')
    