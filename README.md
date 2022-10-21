# DAT640 Group Project 2022H Team-001

This is the project from Team-001 in the 'DAT640-Information retrieval and text mining' course at UiS.

## Directory structure

- `datasets` contains all the datasets
- `evaluate` contains the files to evaluate the datasets
- `0.analysis` contains a Jupyter Notebook which some basic functions to inspect characteristics of the datasets
- `1.baseline` contains the baseline functions and program to run on the datasets

## TODO: write about running each specific directory

## [SeMantic AnsweR Type (SMART)](https://smart-task.github.io/) prediction task

SMART task is a dataset for the answer type prediction task. Question Answering is a popular task in the field of Natural Language Processing and Information Retrieval, in which, the goal is to answer a natural language question (going beyond the document retrieval). Question or answer type classification plays a key role in question answering. The questions can be generally classified based on Wh-terms (Who, What, When, Where, Which, Whom, Whose, Why). Similarly, the answer type classification is determining the type of the expected answer based on the query. Such answer type classifications in literature are performed as a short-text classification task using a set of coarse-grained types, for instance, either 6 or 50 types with TREC QA task. A granular answer type classification is possible with popular Semantic Web ontologies such as DBepdia (~760 classes) and Wikidata (~50K classes).
In this challenge, given a question in natural language, the task is to predict type of the answer using a set of candidates from a target ontology.
