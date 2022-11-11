from functions_indexing import *
from elasticsearch import Elasticsearch

from abstracts_index import INDEX_NAME


###################################################
# THIS FILE IS USED FOR TEMPORARY EXPERIMENTATION #
#                  IGNORE IT                      #
###################################################


def preprocess(doc):
    """Preprocesses a document
    Taken from A2.1 assignment
    """
    ps = PorterStemmer()
    return [ps.stem(term) for term in re.sub(r"[^\w]|_", " ", doc).lower().split()]


if __name__=="__main__":

    es = Elasticsearch()

    ques = 'How many ingredients are in the grain} ?'

    query = preprocess(ques)

    res = es.search(index=INDEX_NAME, q=ques, df="description", _source=False)

    print(res)
    