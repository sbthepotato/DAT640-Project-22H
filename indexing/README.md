# Indexing

TODO: finish README

## Downloading full type dataset

The index functions rely on the presense of a file names `instance_types_en.ttl` to exist in `.datasets/DBpedia`. This file is not here by default because it is quite large (748,7MB) so it must be manually downloaded from [downloads.dbpedia](http://downloads.dbpedia.org/2016-10/). The file can be found by going into `core/` and in the `/core/` directory it can be found with the name `instance_types_en.ttl.bz2`. Simply download this file, unzip it and place it in `../datasets/DBpedia`. Then this code should work.
