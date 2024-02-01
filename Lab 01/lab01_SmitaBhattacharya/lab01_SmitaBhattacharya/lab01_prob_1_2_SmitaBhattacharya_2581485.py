import spacy, re, os, glob, argparse, operator
from bs4 import BeautifulSoup
from unidecode import unidecode
from pathlib import Path
import pandas as pd
from collections import Counter, defaultdict

REF_BLOCKS = re.compile('<ref.*?(<\/ref>|\/>)')
NONTAGGED_REF_BLOCKS = re.compile('{{.*?}}')
MARKED_NAMED_ENTITIES = re.compile('\[\[([^\|]*?)\]\]')
MARKED_TAGGED_NAMED_ENTITIES = re.compile('\[\[(.+?)\|(.+?)\]\]')
COMMENTS = re.compile('<!--.*?-->')
SUBHEADINGS = re.compile('={2,3}.*?={2,3}')
CLASS_BLOCKS = re.compile('\{\| class=(.+?)\|\}')
STYLE_BLOCKS = re.compile('\{\| style=(.+?)\|\}')

def preprocess_data(inp_dir, save_dir):
    '''
    Function to clean the wikipedia dump. Important cleaning steps have been implemented. There might be cases where further cleaning is still required when the dump has complex format with nested divisions/classes and so on.
    '''
    for fname in glob.glob(inp_dir+'/'+'*.txt'):
        ### read the text file
        with open(fname, 'r') as read_ptr:
            text = read_ptr.readlines()
            subject_entity = text[0]
            text = " ".join([t if "[[File:" not in t else '' for t in text]) ### removing the [[File:: ...]] line which has nested brackets
            text = unidecode(text) ### converting non-ascii characters to ascii
            text = text.split('== See also ==')[0] ### removing the footnotes
            text = re.sub('[\']{3}', "####\'\'\'", text, 1).split("####")[1] ### removing header
            text = re.sub(REF_BLOCKS, '', text)
            text = re.sub(NONTAGGED_REF_BLOCKS, '', text)
            text = re.sub(COMMENTS, '', text)
            text = re.sub(SUBHEADINGS, '', text)
            text = re.sub(MARKED_NAMED_ENTITIES, r'\1', text)
            text = re.sub(MARKED_TAGGED_NAMED_ENTITIES, r'\2', text)
            text = re.sub('\s+',' ',text) ### remove extra spaces, tabs, newline
            text = re.sub(CLASS_BLOCKS, '', text) ### remove the {| class= ... |} blocks
            text = re.sub(STYLE_BLOCKS, '', text) ### remove the {| style= ... |} blocks
            text = re.sub('\[\[', '', text) ### finally remove the markup around NER
            text = re.sub('\]\]', '', text) ### finally remove the markup around NER
            ext = re.sub('\{\{', '', text) ### finally remove the markup around NER
            text = re.sub('\}\}', '', text) ### finally remove the markup around NER
            text = re.sub('\(\)', '', text) ### finally remove the markup around NER
            text = re.sub('http[^\s]*', '', text) ### remove urls if present outside the markup tags
            text = re.sub('\'{2,}', '', text) ### only remove the trailing apostrophes
            text = re.sub('<.*?>', '', text) ### other tags
            text = re.sub('\*', '', text) ### remove * punctuation that comes from list type sentences
            text = re.sub('&nbsp;', ' ', text) ### remove non-breaking space tag from the text
            text = text.replace('-', ' ') ### remove - but giving a space to handle multi-token words

            os.makedirs(save_dir+'/', exist_ok=True)
            with open(save_dir+'/'+fname.split('/')[-1], 'w') as write_ptr: ### saving the cleaned text with the same filename
                write_ptr.write(subject_entity)
                write_ptr.write(text)

def problem_1(dir, save_dir):
    nlp = spacy.load('en_core_web_lg')
    os.makedirs(save_dir, exist_ok=True)

    for file in glob.glob(dir+'/'+'*.txt'):
        print (file)
        with open(file, 'r') as read_ptr:
            subject_entity = read_ptr.readline().rstrip() ### reading the first line which contains the subject_entity
            text = read_ptr.read().rstrip() ### reading the rest of the text file
            
            document = nlp(text) ### processing text using Spacy's model
            named_entities = [ents.text.lstrip().rstrip().lower() for ents in document.ents] ### documents.ents has the named-entities. storing it in lower form to get the accurate frequency
            
            frequency_list = sorted(Counter(named_entities).items(), key=operator.itemgetter(1), reverse=True) ### counter function to convert a list into dictionary of count and then sorting the dictionary in the descending order based on the count
            
            df = pd.DataFrame(frequency_list, columns=['Named-entity', 'Frequency']) ### converting the list of tuples into pandas dataframe
            df.insert(loc=0, column='Title', value=[subject_entity]*len(df)) ### inserting the column containing the subject_entity
            df.to_csv(save_dir+'/'+subject_entity.replace(' ', '_')+'.csv', index=False) ### saving in csv format
    
    print ('Solved problem 1 !!!')

def problem_2_1(dir, save_dir):
    nlp = spacy.load('en_core_web_lg')
    os.makedirs(save_dir, exist_ok=True)
    
    df = pd.DataFrame() ### single dataframe to store all the frequenct verbs and adjectives
    
    for file in glob.glob(dir+'/'+'*.txt'):
        print (file)
        with open(file, 'r') as read_ptr:
            subject_entity = read_ptr.readline().rstrip() ### reading the first line which contains the subject_entity
            text = read_ptr.read().rstrip() ### reading the rest of the text file
            
            document = nlp(text) ### processing text using Spacy's model
            verbs = [token.lemma_ for token in document if token.pos_ == 'VERB'] ### token.pos_ gives the parts of speech tag. since we need verbs, so match with 'VERB' 
            adjectives = [token.lemma_ for token in document if token.pos_ == 'ADJ'] ### token.pos_ gives the parts of speech tag. since we need adjectives, so match with 'ADJ' 

            frequent_verbs = sorted(Counter(verbs).items(), key=operator.itemgetter(1), reverse=True)[:5] ### using Counter to get dictionary of verb counts and then sorting to pick the top 5 verbs 
            frequent_adjectives = sorted(Counter(adjectives).items(), key=operator.itemgetter(1), reverse=True)[:5] ### using Counter to get dictionary of adjective counts and then sorting to pick the top 5 adjectives 

            verb_df = pd.DataFrame(frequent_verbs, columns=['POS', 'Frequency'])
            verb_df.insert(loc=0, column='Title', value=[subject_entity]*len(verb_df))
            verb_df.insert(loc=1, column='POS Type', value=['verb']*len(verb_df))

            adj_df = pd.DataFrame(frequent_adjectives, columns=['POS', 'Frequency'])
            adj_df.insert(loc=0, column='Title', value=[subject_entity]*len(adj_df))
            adj_df.insert(loc=1, column='POS Type', value=['adjective']*len(adj_df))

            df = pd.concat([df, verb_df])
            df = pd.concat([df, adj_df])

    df.to_csv(save_dir+'/'+'Problem2_1.csv', index=False)
    print ('Solved problem 2.1 !!!')

def problem_2_2(dir, save_dir):
    nlp = spacy.load('en_core_web_lg')
    os.makedirs(save_dir, exist_ok=True)

    for file in glob.glob(dir+'/'+'*.txt'):
        print (file)
        with open(file, 'r') as read_ptr:
            subject_entity = read_ptr.readline().rstrip() ### reading the first line which contains the subject_entity
            text = read_ptr.read().rstrip() ### reading the rest of the text file
            
            document = nlp(text) ### processing text using Spacy's model
            named_entity_to_sent_mapping = defaultdict(list) ### key: named-entity, val: list of sentences
            for named_entities in document.ents:
                named_entity_to_sent_mapping[named_entities.text.lstrip().rstrip().lower()].append(named_entities.sent) ### mapping each identified named-entity to it's source sentence using a dictionary
            
            named_entity_to_sent_mapping = dict(named_entity_to_sent_mapping)
            df = pd.DataFrame({'Sentences':named_entity_to_sent_mapping}).rename_axis('Named-entity').reset_index() ### creating a dataframe with list of sentences as a cell value and dict key as index
            df = df.explode('Sentences').sort_values(by='Named-entity') ### exploding the dataframe with each row containing only one source sentence
            df.insert(loc=0, column='Title', value=[subject_entity]*len(df)) ### inserting the column containing the subject_entity
            
            df.to_csv(save_dir+'/'+subject_entity.replace(' ', '_')+'.csv', index=False) ### saving in csv format
   
    print ('Solved problem 2.2 !!!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir", help="Wikipedia dump directory", required=True, type=str)
    parser.add_argument("-o", "--output_dir", help="Preprocessed text directory", required=True, type=str)
    args = parser.parse_args()

    preprocess_data(args.input_dir, args.output_dir)
    problem_1(args.output_dir, 'Problem1')
    problem_2_1(args.output_dir, 'Problem2_1')
    problem_2_2(args.output_dir, 'Problem2_2')