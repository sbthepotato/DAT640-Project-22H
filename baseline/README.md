# Baseline method

The baseline method is a simple BM25 score on the DBpedia dataset by comparing it to the DBpedia training dataset. The functions have been commented on and so has the code to explain the logic.

## Files

- `requirements.txt` This has all the non standard python libraries used and their version. Run `pip install -r requirements.txt` to install them. It does not check the Python version but anything over 3.7 *should* work. I ran it with 3.9.13.
- `base.py` Run this to do the category and type prediction on the DBpedia dataset, assuming the package requirements have been met and the directory structure hasn't been changed this should work out of the box.
- `functions_base.py` Contains all the functions used in `base.py`

## Evaluation results

Category prediction (based on 4369 questions)

&emsp;&emsp; Accuracy: 0.342

Type ranking (based on 4369 questions)

&emsp;&emsp; NDCG@5:  0.113

&emsp;&emsp; NDCG@10: 0.112
