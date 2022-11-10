# Baseline method

The baseline method for category prediction is a simple BM25 score on the DBpedia dataset by comparing it to the DBpedia and Wikidata training datasets.

The type prediction is done with a simple BM25 score on the indexed DBpedia dump.

The functions have been commented on and so has the code to explain the logic.

## Files

- `category_base.py` Run this to do the category prediction and type prediction for `literal` and `boolean` categories. If package requirements have been met and the directory structure hasn't been changed this should work out of the box.
- `functions_base.py` Contains all the functions used in `category_base.py` and `type_base.py`
- `requirements.txt` This has all the non standard python libraries used and their version. Run `pip install -r requirements.txt` to install them. It does not check the Python version but anything over 3.7 *should* work. I ran it with 3.9.13.
- `type_base.py` Run this to do the type prediction on the DBpedia dataset for all `resource` types. **NOTE: Indexing needs to be run for this to work, go to `../indexing` for instructions.** If package requirements have been met and the directory structure hasn't been changed this should work out of the box.

## Evaluation results

### Category prediction, no type prediction

&emsp;Category prediction (based on 4369 questions)

&emsp;&emsp; Accuracy: 0.514

&emsp;Type ranking (based on 4369 questions)

&emsp;&emsp; NDCG@5:  0.027

&emsp;&emsp; NDCG@10: 0.027

### Category and type prediction

&emsp;Category prediction (based on 4369 questions)

&emsp;&emsp; Accuracy: 0.X

&emsp;Type ranking (based on 4369 questions)

&emsp;&emsp; NDCG@5:  0.Y

&emsp;&emsp; NDCG@10: 0.Z
