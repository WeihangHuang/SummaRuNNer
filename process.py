'''
This code is used to create article and summary files from the csv file.
The code is the modified version of process.py in https://github.com/mahnazkoupaee/WikiHow-Dataset.git
The output of the file will be a JSON file with fields "doc", "summaries" and "labels".
"doc" is the article, "summaries" is the summary and "labels" is some random input, as it's not used
during evalutaion.
'''
import pandas as pd
import os
import re
import simplejson

def handle_article(article):
    # remove all newline symbles:
    processed_article = article.replace('\n', '')

    # replace all period with newline symbles:
    processed_article = processed_article.replace('. ', '\n')

    # remove the first empty space
    processed_article = processed_article[1:]

    # count the number of sentences and create the labels
    sents_num = processed_article.count('\n') + 1
    labels = '\n'.join(['0' for _ in range(sents_num)])
    
    # encode to utf-8
    # processed_article = processed_article.encode('utf-8')
    # labels = labels.encode('utf-8')

    return processed_article, labels

# read data from the csv file (from the location it is stored)
Data = pd.read_csv(r'wikihowAll.csv')
Data = Data.astype(str)
rows, columns = Data.shape

# create a file to record the file names. This can be later used to divide the dataset in train/dev/test sets
title_file = open('titles.txt', 'wb')
json_file = open('data/wikihow_eval.json', 'w', encoding='utf8')

# go over the all the articles in the data file
for row in range(rows):
    abstract = Data.ix[row,'headline']      # headline is the column representing the summary sentences
    article = Data.ix[row,'text']           # text is the column representing the article

    #  a threshold is used to remove short articles with long summaries as well as articles with no summary
    if len(abstract) < (0.75*len(article)):
        # remove extra commas in abstracts
        abstract = abstract.replace("\n","")
        abstract = abstract.replace(".,", "")

        # remove extra commas in articles
        article = re.sub(r'[.]+[\n]+[,]',".", article)
        # process on the main article
        processed_article, labels = handle_article(article)       
        
        # file names are created using the alphanumeric charachters from the article titles.
        # they are stored in a separate text file.
        filename = Data.ix[row,'title']
        filename = "".join(x for x in filename if x.isalnum())
        filename1 = filename + '.txt'
        filename = filename.encode('utf-8')
        title_file.write(filename+b'\n')

        # make a json dict
        data = {}
        
        # remove the last symble in the abstract
        abstract = abstract[:-1]

        # add the abstract into json data as summaries
        data['summaries'] = abstract

        # add article
        data['doc'] = processed_article
        data['labels'] = labels

        # dump and write the data
        simplejson.dump(data, json_file, ensure_ascii=False)
        json_file.write('\n')

title_file.close()
json_file.close()


    
