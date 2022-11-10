# Indexing

**NOTE: To run these files some datasets which are not included by default need to be downloaded. Instructions can be found in `../datasets/DBpedia/`**

**NOTE: These use a lot of memory, if python is terminating on its own then you need to decrease the number of splits in the multiprocessing. All files have a `nr_splits` variable near the top of the file. Change this to some lower value and try again if you're having issues.**

## Files

- `abstract_long_index.py` - Run this to index the `long_abstracts_en.ttl` file
- `abstract_short_index.py` - Run this to index the `short_abstracts_en.ttl` file
- `functions_index.py`  - Contains all the functions used in the indexing files
- `instance_index.py` - Run this to index the `instace_types_en.ttl` file
- `requirements.txt` - Required packages, run `pip install -r requirements.txt` to install. For the other files anything above Python 3.7 should work. I used 3.9.13

## Downloading Instance types and Abstracts datasets

Instructions to download the datasets can be found in `../datasets/DBpedia/`
