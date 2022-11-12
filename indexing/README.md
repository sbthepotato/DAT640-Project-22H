# Indexing

**NOTE: To run these files some datasets which are not included by default need to be downloaded. Instructions can be found in `../datasets/DBpedia/`**

**NOTE: Make sure you have downloaded and run `elasticsearch` as detailed in the `README` in the root directory.**

## Files

- `abstract_clean.py` - Run this to clean the `long_abstracts_en.ttl` file and create a JSON file of it
- `abstracts_index.py` - Run this to index the JSON file from `abstact_clean.py`
- `functions_index.py`  - Contains all the functions used in the indexing files
- `instance_clean.py` - Run this to clean the `instace_types_en.ttl` file and create a JSON file of it
- `instances_index.py` - Run this to index the JSON file from `instance_clean.py`
- `requirements.txt` - Required packages, run `pip install -r requirements.txt` to install. For the other files anything above Python 3.7 should work. I used 3.9.13
- `train_index.py` - Run this to index the training datasets

## Run order / instructions

After the necessary files have been downloaded the files in this directory should be run in the following order:

1. `train_index.py`
2. `instance_clean.py`
3. `instances_index.py`
4. `abstract_clean.py`
5. `abstracts_index.py`

**If you run these files out of order some functions will not work!**

if you want to index the short abstracts instead of the long one you have to go into the `abstracts_clean.py` file and uncomment line `15` and comment line `16`

## Elasticsearch

Besides the presence of elasticsearch in the `requirements.txt` file it also needs to be downloaded and run separately. Instructions can be found in the root directory' `README.md` file.

## Downloading Instance types and Abstracts datasets

Instructions to download the datasets can be found in `../datasets/DBpedia/`

## Logic of the order

`train_index.py` doesn't rely on any of the other files and no files rely on it so technically it doesn't matter. I put it first in the list just because.

`instance_clean.py` will clean the `instance_types_en.ttl` file. It does this by extracting the first element which is the ID of the type. It also removes number at the end of it in case of it having multiple types and combines the types into a single element. This has to be run before `instances_index.py` because `instances_index.py` reads the cleaned output file from `instance_types_en.ttl`.

`abstract_clean.py` cleans the `long_abstracts_en.ttl` file. it also extracts the first element as the ID and then preprocesses the 3rd field as the description.

The important thing is that `abstracts_index.py` is run after all these other files because it relies both on the `abstracts_clean.py` to have been run and the `instances_index.py`. This is because we will only index entries which actually have types associated with them since they're the only ones we're interested in. We only know which ID's have types after running the `instances_index.py`.
