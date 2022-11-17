# Advanced method

**NOTE: Indexing needs to be run for this to work, go to `../indexing/` for instructions.**

**NOTE: Elasticsearch needs to be running for this to work, go to the root directory for instructions.**

Advanced method uses the same BM25 scoring as in the baseline method, we additionally re-weigh the scores based on the the first word in each question and we add the types from the training dataset.

## files

- `advanced.py` Run this to do the category and type prediction on the DBpedia dataset, assuming the package requirements have been met and the directory structure hasn't been changed this should work out of the box.
- `functions_advanced.py` Contains all the methods used to actually classify questions, some old from baseline, some modified and some new.
- `functions_base.py` Contains the basic functions from baseline that don't directly answer the query
- `requirements.txt` This has all the non standard python libraries used and their version. Run `pip install -r requirements.txt` to install them. It does not check the Python version but anything over 3.7 *should* work. I ran it with 3.9.13.

## Evaluation results

### Category prediction improvements

&emsp;Category prediction (based on 4369 questions)

&emsp;&emsp; Accuracy: 0.940

&emsp;Type ranking (based on 4369 questions)

&emsp;&emsp; NDCG@5:  0.499

&emsp;&emsp; NDCG@10: 0.501

### Category & Type prediction improvements

&emsp;Category prediction (based on 4369 questions)

&emsp;&emsp; Accuracy: 0.940

&emsp;Type ranking (based on 4369 questions)

&emsp;&emsp; NDCG@5:  0.524

&emsp;&emsp; NDCG@10: 0.538
