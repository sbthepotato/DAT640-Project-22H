# DBpedia

## Files

### Need to be downloaded / generated

- `dbpedia_abstracts.json` - **Needs to be generated, instructions are in the `../../indexing/` directory** - contains the contents of `long_abstracts_en.ttl` which have been processed and cleaned
- `dbpedia_instance_types.json` - **Needs to be generated, instructions are in the `../../indexing/` directory** - contains the contents of `instance_types_en.ttl` which have been cleaned and sorted

- `instance_types_en.ttl` - **Needs to be downloaded, instructions below** - contains the types of a given DBpedia instance
- `long_abstracts_en.ttl` - **Needs to be downloaded, instructions below** - contains the long description of a given DBpedia instance

### Included
  
- `smarttask_dbpedia_test_questions.json` - contains the questions that need to be classified
- `smarttask_dbpedia_test.json` - contains the correct category and type for each question
- `smarttask_dbpedia_train.json` - contains the training dataset
- - `smarttask_dbpedia_test_answers_advanced.json` - contains the category and type predictions from the advanced method
- `smarttask_dbpedia_test_answers_base.json` - contains the category and type predictions from the baseline method

## Optional files

The indexing is slightly faster if you index the short abstracts instead of the long ones. Note that the results will probably be worse. If you do this you need to change one of the indexing functions, instructions will be in the `../../indexing/` directory.

- `short_abstracts_en.ttl` - **Needs to be downloaded, instructions below** - contains the short description of a given DBpedia instance

## Downloading the missing datasets

The missing datasets are quite large so they have not been included in the commit. They can be found at [downloads.dbpedia.org/2016-10/](http://downloads.dbpedia.org/2016-10/).

The files can be found by going into `core/` and in that directory they can be found with the names `instance_types_en.ttl.bz2`, `long_abstracts_en.ttl.bz2` and `short_abstracts_en.ttl.bz2`.

After downloading these datasets they need to be unzipped and put in this directory with the exact file names as given above. The functions in `../../indexing` **will not work** if you change the file names or don't place the files correctly.
