# -*- coding: utf-8 -*-
"""
Created on Wed May  4 16:10:25 2022

@author: study
"""

import csv
import requests
import re

from bs4 import BeautifulSoup
from pprint import pprint
from typing import Dict, List, Union


def problem_1(source) -> List[Dict[str, Union[str, List[str]]]]:
   
    source1 ="https://how-i-met-your-mother.fandom.com/wiki/"
    s=source
    new_s = s.replace(" ", "_")
    final_s=source1+new_s
    source2=requests.get(final_s).text
    doc = BeautifulSoup(source2, "html.parser")
    tbody= doc.find('table', class_="infobox character")
    trs= tbody.find_all('tr')[2:-1]
    
    full_info = []
    dict_1 = {}
    final= []
    for tr in trs:
        divs = tr.find_all('div')
        key = divs[0].text
        value = divs[1].text
        final.append({key: value})

    return final
        
    
    
def problem_2_1() -> List[Dict[str, str]]:
    
    base_url = "https://www.lsf.uni-saarland.de/qisserver/rds?state=wtree&search=1&trex=step&root120221=320944|310559|318658|311255&P.vx=kurz&noDBAction=y&init=y&language=en"
    
    source=requests.get(base_url).text
    content= BeautifulSoup(source, "html.parser")
    divContent= content.find('div', class_="divcontent")
    tableAll= divContent.find_all('table')[10:]
    CourseAll=[]

    for t in tableAll:
        if t.find('table'):
            continue
        a=t.find('a').get("href")
        source_C= requests.get(a).text
        content_C=BeautifulSoup(source_C, "html.parser")
        table= content_C.find('table', summary="Übersicht über alle Veranstaltungen")
        trs=table.find_all('tr')[1:]
        for tr in trs:
            tds=tr.find_all('td')[1]
            link=tds.find('a').get('href')
            text=tds.find('a').text
            CourseAll.append({'Name of Course':text, 'URL':link})            
        
    #print(type(CourseAll))
    return CourseAll


def problem_2_2(url: str) -> Dict[str, Union[str, List[str]]]:
   
    base_url2= url
    source2=requests.get(base_url2).text
    content2= BeautifulSoup(source2,"html.parser")
    divContent2= content2.find('div', class_="divcontent")
    table2=divContent2.find('table', summary="Grunddaten zur Veranstaltung")
    trs2=table2.find_all('tr')
    final={}
    for tr2 in trs2[:5]:
        th=tr2.find_all('th')
        td=tr2.find_all('td')
        final.update({th[0].text: td[0].text.strip()})
        final.update({th[1].text: td[1].text.strip()})
    for tr2 in trs2[5:-1]:
        th = tr2.find('th')
        td = tr2.find('td')
        final.update({th.text.strip(): td.text.strip()})
    
    table22=divContent2.find('table', summary="Verantwortliche Dozenten")
    table22_trs= table22.find_all('tr')[1:]
    temp = []
    for tr in table22_trs:
        td = tr.find('td')
        text=td.find('a').text.strip()
        temp.append(text)
    final.update({'Responsible Instructor':temp})
    
    return final


def problem_2_3() -> None:
    
    problem_2_2("https://www.lsf.uni-saarland.de/qisserver/rds?state=verpublish&status=init&vmfile=no&publishid=136473&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung&language=en")
    return None


def main():
    # You can call your functions here to test their behaviours.
    #pprint(problem_1("Tracy McConnell"))
    #pprint(problem_2_1())
    pprint(problem_2_2("https://www.lsf.uni-saarland.de/qisserver/rds?state=verpublish&status=init&vmfile=no&publishid=136388&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung&language=en"))
    #pprint(problem_2_3())
    #pprint(problem_1("Lily Aldrin"))


if __name__ == "__main__":
    main()