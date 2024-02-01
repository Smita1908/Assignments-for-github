'''
Created on Nov 8, 2019
Sample structure of run file run.py

@author: cxchu
'''

import sys
import spacy
import csv
import pandas as pd

def your_typing_function():
    
    '''
    This function reads the input file (e.g. test.tsv)
    and does typing all given entity mentions.
    The results is saved in the result file (e.g. results.tsv)
    '''
    nlp=spacy.load('en_core_web_sm')
    #print(nlp.pipe_names)
    ner=nlp.get_pipe("ner")
    fout = open("result_file.tsv", 'w', encoding='utf8')
    fin = open("train.tsv", 'r', encoding='utf8')
    formatting1= []
    formatting2=[]
    for line in fin.readlines():
        comps = line.rstrip().split("\t")
        sentence = comps[2]
        id= len(comps[0])
        entity = comps[1]
        formatting1.append(0)
        formatting1.append(id)
        formatting1.append(entity)
        formatting2.append({'entites:':formatting1})
        print(formatting2)    
    '''
    entities= []
    labels = []
    position_start= []
    position_end= []
    for line in fin.readlines():
        comps = line.rstrip().split("\t")
        id = comps[0]
        lenght_id= len(id)
        entity = comps[1]
        sentence = comps[2]
        doc=nlp(sentence)
        for ent in doc.ents:
            entities.append(ent)
            labels.append(entity)
            position_start.append(ent.start_char)
            position_end.append(ent.end_char)
  
        ## radomly return a 7th word in the sentence as a type
        ## else the first word if the length of the sentence < 7
        words = sentence.split(' ')
        types = []
        if len(words) > 7:
            types.append(words[7])
            #print(types)
        else:
            types.append(words[0])
        #fout.write(str(id) + "\t" + str(types) + "\n")
    #fout.close()
    #print(len(entity_type))
    df= pd.DataFrame({'Entities':entities, 'Labels':labels, 'Position_start':position_start, 'Position_End':position_end})
    print(df)
    print("##") 
    '''
'''
*** other code if needed
'''    
    
    
'''
main function
'''
if __name__ == '__main__':
    #if len(sys.argv) != 3:
        #raise ValueError('Expected exactly 2 argument: input file and result file')
    #your_typing_function(sys.argv[1], sys.argv[2])
    your_typing_function()
