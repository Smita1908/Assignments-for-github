'''
Created on Nov 25, 2019
Sample structure of run file run.py

@author: cxchu
'''

import sys
from typing import Any, Dict

import spacy


nlp = spacy.load("en_core_web_sm")

def your_extracting_function(input_file, result_file):
    '''
    This function reads the input file (e.g. sentences.tsv)
    and extracts all SPO per line.
    The results are saved in the result file (e.g. results.txt)
    '''
    with open(result_file, 'w', encoding='utf8') as fout:
        with open(input_file, 'r', encoding='utf8') as fin:
            id = 1
            for line in fin:
                line = line.rstrip()
                
                '''
                baseline: running dependency, return head verb, nominal subject and directed object
                comment out or remove when running your code
                verbs = {key: {'subject': text, 'object': text}}
                '''
                verbs = spo_baseline(line)
                        
                '''
                end baseline
                '''

                '''
                Extracting SPO
                === your code goes here ===
                verbs = extract_spo(line)
                '''

                '''
                formatiing dict compatible with oie reader
                '''
                if len(verbs) > 0:
                    res = ''
                    for key, value in verbs.items():
                        if value['subject'] != '' and value['object'] != '':
                            res += str(id) + '\t"' + value["subject"] + '"\t"' + key + '"\t"' + value["object"] + '"\t0\n'
                    if res != '':
                        fout.write(line + "\n")
                        fout.write(res) 
                        id += 1


'''
baseline implementation
'''
def spo_baseline(line):
    verbs = {}
    doc = nlp(line)
    s_verb = ''
    for token in doc:
        key = token.head.text
        if(token.head.pos_ == "VERB" and key not in verbs.keys()):
            s_verb = key
            verbs[key] = {"subject":"","object":""}
        if(token.dep_ == "nsubj" and token.head.pos_ == "VERB"):
            verbs[key]["subject"] = token.text
        elif(token.dep_ == "dobj" and token.head.pos_ == "VERB"):
            verbs[key]["object"] = token.text

    if s_verb:
        if s_verb in verbs:
            if verbs[s_verb]['subject'] == '' or verbs[s_verb]['object'] == '':
                verbs = spo(line, s_verb, verbs)
    return verbs


'''
*** other code if needed

'''


def spo(line, key, verb):
    doc = nlp(line)
    docl = line.split(' ')
    if key in docl:
        pos = docl.index(key)
    else:
        return verb
    for i, token in enumerate(doc):
        if i < pos and token.pos_ == 'NOUN':
            verb[key]["subject"] = token.text
        if i > pos and token.pos_ == 'NOUN':
            verb[key]["object"] = token.text
    return verb


'''
main function
'''
if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError('Expected exactly 2 argument: input file and result file')
    your_extracting_function(sys.argv[1], sys.argv[2])
    #sentence = "Annualized interest rates on certain investments as reported by the Federal Reserve Board on a weekly - average basis :"
    #spo_baseline(sentence)
    #print(spo(sentence))
