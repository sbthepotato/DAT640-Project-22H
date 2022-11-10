# Advanced method

TBA TODO

## files

- `advanced.py` Run this to do the category and type prediction on the DBpedia dataset, assuming the package requirements have been met and the directory structure hasn't been changed this should work out of the box.
- `requirements.txt` This has all the non standard python libraries used and their version. Run `pip install -r requirements.txt` to install them. It does not check the Python version but anything over 3.7 *should* work. I ran it with 3.9.13.
- `functions_advanced.py` Contains all the new and modified functions used in the advanced method
- `functions_base.py` Contains functions used in `advanced.py` that were not modified at all from how they look like in the baseline method

## Evaluation results

&emsp;Category prediction (based on 4369 questions)

&emsp;&emsp; Accuracy: 0.X

&emsp;Type ranking (based on 4369 questions)

&emsp;&emsp; NDCG@5:  0.Y

&emsp;&emsp; NDCG@10: 0.Z
