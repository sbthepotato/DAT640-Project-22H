# Indexing

**NOTE: To run these files some datasets which are not included by default need to be downloaded. Instructions can be found in `../datasets/DBpedia/`**

**NOTE: These can use a lot of memory, if python is terminating on its own then you need to decrease the number of splits in the multiprocessing. All files use the `SPLITS` variable in `functions_indexing.py`. Change this to some lower value and try again if you`re having issues.**

**NOTE: Make sure you have downloaded and run `elasticsearch` as detailed in the `README` in the root directory.**

## Files

- `abstract_clean.py` - Run this to clean the `long_abstracts_en.ttl` file and create a JSON file of it
- `abstracts_index.py` - Run this to index the JSON file from `abstact_clean.py`
- `functions_index.py`  - Contains all the functions used in the indexing files
- `instance_clean.py` - Run this to clean the `instace_types_en.ttl` file and create a JSON file of it
- `instances_index.py` - Run this to index the JSON file from `instance_clean.py`
- `requirements.txt` - Required packages, run `pip install -r requirements.txt` to install. For the other files anything above Python 3.7 should work. I used 3.9.13

## Elasticsearch

Besides the presence of elasticsearch in the `requirements.txt` file it also needs to be downloaded and run separately. Instructions can be found in the root directory' `README.md` file.

## Downloading Instance types and Abstracts datasets

Instructions to download the datasets can be found in `../datasets/DBpedia/`
