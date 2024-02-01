# -*- coding: utf-8 -*-
"""
Created on Wed May 11 17:34:31 2022

@author: study
"""

import spacy
from spacy import displacy
import pandas as pd
spacy.__version__

nlp=spacy.load("en_core_web_sm")

text="Apple acquired Zoom in China on Wedesday 6th May,2020.\
    This news has made Apple and Google stock jump by 5% on Dow Jones Index in the\
    United States of America"
    
doc= nlp(text)

entities= []
labels= []
position_start= []
position_end= []

for ent in doc.ents:
    entities.append(ent)
    labels.append(ent.label_)
    position_start.append(ent.start_char)
    position_end.append(ent.end_char)

df= pd.DataFrame({'Entities':entities, 'Labels':labels, 'Position_start':position_start, 'Position_End':position_end})

print(df)
