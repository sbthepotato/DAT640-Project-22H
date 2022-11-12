# Baseline method

**NOTE: Indexing needs to be run for this to work, go to `../indexing/` for instructions.**

**NOTE: Elasticsearch needs to be running for this to work, go to the root directory for instructions.**

The baseline method uses the BM25 scoring built into Elasticsearch on the DBpedia questions by comparing it to the DBpedia and Wikidata training datasets. The first comparison will establish the category and type if the category is 'boolean' or 'literal'.

The baseline method will again use the built in BM25 scoring on the dbpedia `long_abstracts_en.ttl` dataset to establish the types for a given resource

The functions have been commented on and so has the code to explain the logic.

## Files

- `base.py` Run this to do category and type prediction for the DBpedia dataset. if the package requirements have been met, the directory structure hasn't changed, everything has been indexed as detailed and Elasticsearch is running then this should work without further modifications.
- `functions_base.py` Contains all the functions used in `base.py`
- `requirements.txt` This has all the non standard python libraries used and their version. Run `pip install -r requirements.txt` to install them. It does not check the Python version but anything over 3.7 *should* work. I ran it with 3.9.13.

## Evaluation results

&emsp;Category prediction (based on 4369 questions)

&emsp;&emsp; Accuracy: 0.916

&emsp;Type ranking (based on 4369 questions)

&emsp;&emsp; NDCG@5:  0.393

&emsp;&emsp; NDCG@10: 0.393
