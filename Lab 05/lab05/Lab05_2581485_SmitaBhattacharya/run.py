'''
Created on Nov 25, 2019
Sample structure of run file run.py

@author: cxchu
@editor: ghoshs
'''

import sys
import re
import csv
from datetime import datetime
import datefinder
import spacy


nlp = spacy.load("en_core_web_sm")

def your_extracting_function(input_file, result_file):
    
    '''
    This function reads the input file (e.g. input.csv)
    and extracts the required information of all given entity mentions.
    The results is saved in the result file (e.g. results.csv)
    '''
    with open(result_file, 'w', encoding='utf8') as fout:
        headers = ['entity','dateOfBirth','nationality','almaMater','awards','workPlaces']
        writer = csv.writer(fout, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        
        with open(input_file, 'r', encoding='utf8') as fin:
            reader = csv.reader(fin)

            # skipping header row
            next(reader)
            
            for row in reader:
                entity = row[0]
                abstract = row[1]
                dateOfBirth, nationality, almaMater, awards, workPlace = [], [], [], [], []
                
                '''
                baseline: adding a random value 
                comment this out or remove this baseline 
                
                dateOfBirth.append('1961-1-1')
                nationality.append('United States')
                almaMater.append('Johns Hopkins University')
                awards.append('Nobel Prize in Physics')
                workPlace.append('Johns Hopkins University')
                '''
                
                '''
                extracting information 
                '''

                dateOfBirth += extract_dob(entity, abstract)
                nationality += extract_nationality(entity, abstract)
                almaMater += extract_almamater(entity, abstract)
                awards += extract_awards(entity, abstract)
                workPlace += extract_workpace(entity, abstract)
                
                writer.writerow([entity, str(dateOfBirth), str(nationality), str(almaMater), str(awards), str(workPlace)])
        
    
'''
date of birth extraction function
'''    

def extract_dob(entity, abstract, **kwargs):
    dob = []
    entity_dob = entity
    abstract_dob = abstract

    matches_dob = datefinder.find_dates(abstract_dob)

    temp = []
    dob1 = []
    for match in matches_dob:
        temp.append(match)
    if len(temp) == 0:
        pass
    else:
        dob1 = str(temp[0]).split(' ')
        dob.append(dob1[0])

    return dob


'''
nationality extraction function
'''
def extract_nationality(entity, abstract, **kwargs):
    nationality = []
    places = nlp(str(abstract))
    for ent in places.ents:
        if str(ent.label_) == "GPE":
            nationality.append(ent.text)
    return nationality
 

'''
alma mater extraction function
'''
def extract_almamater(entity, abstract, **kwargs):
    almaMater = []
    places = nlp(str(abstract))
    for ent in places.ents:
        if str(ent.label_) == "ORG":
            almaMater.append(ent.text)
    return almaMater


'''
awards extracttion function
'''
def extract_awards(entity, abstract, **kwargs):
    awards = []
    '''
    === your code goes here ===
    '''
    return awards


'''
workplace extraction function
'''
def extract_workpace(entity, abstract, **kwargs):
    workPlace = []
    places = nlp(str(abstract))
    for ent in places.ents:
        if str(ent.label_) == "ORG":
            workPlace.append(ent.text)
    return workPlace


'''
main function
'''
if __name__ == '__main__':

    if len(sys.argv) != 3:
        raise ValueError('Expected exactly 2 argument: input file and result file')
    your_extracting_function(sys.argv[1], sys.argv[2])
    '''
    entity = 'Harold Marshall (acoustician)'
    description = 'Sir Arthur Harold Marshall, KNZM, FRSNZ, FNZIA, FASA (born 15 September 1931) is an expert in acoustics design and research. He is Professor Emeritus of the University of Auckland School of Architecture, and co-founder of Marshall Day Acoustics Ltd in 1981 with Chris Day. He currently resides in Auckland New Zealand, and continues work with Marshall Day Acoustics as a group consultant. He is recognised internationally for his contribution to concert hall design, in particular his seminal work with Mike Barron on the importance of lateral reflections. Currently he is involved in several major concert hall projects including the Guangzhou Opera House with architect Zaha Hadid and the Philharmonie de Paris with French architect Jean Nouvel.'
    print(extract_nationality(entity, description))
    '''
