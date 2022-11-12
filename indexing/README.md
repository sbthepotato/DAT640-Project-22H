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
