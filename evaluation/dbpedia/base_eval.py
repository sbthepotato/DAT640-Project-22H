from evaluate import *

if __name__=="__main__":
    # load everything
    type_hierarchy, max_depth = load_type_hierarchy('dbpedia_types.tsv')
    ground_truth = load_ground_truth('../../datasets/DBpedia/smarttask_dbpedia_test.json', type_hierarchy)
    system_output = load_system_output('../../datasets/DBpedia/smarttask_dbpedia_test_answers_base.json')

    # evaluate it
    evaluate(system_output, ground_truth, type_hierarchy, max_depth)
