"""
Barebone code created by: Tuan-Phong Nguyen
Date: 2022-06-03
"""
import logging
from collections import Counter
from typing import Dict, List, Tuple
import spacy
from spacy.matcher import Matcher
import re

logger = logging.getLogger(__name__)
nlp = spacy.load("en_core_web_sm")

def your_solution(animal: str, doc_list: List[Dict[str, str]]) -> List[Tuple[str, int]]:
    """
    Task: Extract things that the given animal eats. These things should be mentioned in the given list of documents.
    Each document in ``doc_list`` is a dictionary with keys ``animal``, ``url``, ``title`` and ``text``, whereas
    ``text`` points to the content of the document.

    :param animal: The animal to extract diets for.
    :param doc_list: A list of retrieved documents.
    :return: A list of things that the animal eats along with their frequencies.
    """

    print(f"Animal: \"{animal}\". Number of documents: {len(doc_list)}.")

    # You can directly use the following list of documents, which is a list of str, if you don't need other information (i.e., url, title).
    documents = [doc["text"] for doc in doc_list]

    # TODO Implement your own method here
    # You must extract things that are explicitly mentioned in the documents.
    # You cannot use any external CSK resources (e.g., ConceptNet, Quasimodo, Ascent, etc.).
    matcher = Matcher(nlp.vocab)
    pattern = [
       {"LOWER": {"IN": [f"{animal}", f"{animal}s"]}},
        {"LEMMA": "eat"},
        {"POS": "NOUN"}]
    pattern9 = [
       {"LOWER": {"IN": [f"{animal}", f"{animal}s"]}},
        {"POS": "AUX", "OP": "*"},
        {"LEMMA": "eat"},
        {"POS": "NOUN"}]

    pattern1 = [
        {"LOWER": {"IN": [f"{animal}", f"{animal}s"]}},
        {"LEMMA": "consume"},
        {"POS": "NOUN"}]
    pattern10 = [
       {"LOWER": {"IN": [f"{animal}", f"{animal}s"]}},
        {"POS": "AUX", "OP": "*"},
        {"LEMMA": "consume"},
        {"POS": "NOUN"}]

    pattern2 = [
        {"LOWER": {"IN": [f"{animal}", f"{animal}s"]}},
        {"LEMMA": "diet"},
        {"TEXT": "consist of"},
        {"POS": "NOUN"}
        ]

    pattern3 = [
        {"LOWER": {"IN": [f"{animal}", f"{animal}s"]}},
        {"LEMMA": "ingest"},
        {"POS": "NOUN"}]

    pattern4 = [
        {"POS": "PROP"},
        {"LEMMA": "swallow"},
        {"POS": "NOUN"}]

    pattern5 = [
        {"POS":"PROP" },
        {"LEMMA": "diet"},
        {"TEXT": "consists of"},
        {"POS": "NOUN"}
        ]

    pattern6 = [
        {"LOWER": {"IN": [f"{animal}", f"{animal}s"]}},
        {"LEMMA": "bite"},
        {"POS": "NOUN"}
        ]

    pattern7 = [
        {"POS": "PROP"},
        {"LEMMA": "feed"},
        {"POS": "NOUN"}
        ]
    pattern8 = [
        {"LOWER": {"IN": [f"{animal}", f"{animal}s"]}},
        {"LEMMA": "feed"},
        {"POS": "ADP"},
        {"POS": "NOUN"}
        ]

    matcher.add("eatPattern", [pattern])
    matcher.add("consumePattern", [pattern1])
    matcher.add("dietPattern", [pattern2])
    matcher.add("ingestPattern", [pattern3])
    matcher.add("swallowPattern", [pattern4])
    matcher.add("consistsPattern", [pattern5])
    matcher.add("bitePattern", [pattern6])
    matcher.add("feedPPattern", [pattern7])
    matcher.add("feedPattern", [pattern8])
    matcher.add("eat*Pattern", [pattern9])
    matcher.add("consume*Pattern", [pattern10])

    logger.info(
        f"Animal: \"{animal}\". Number of documents: {len(doc_list)}. Running SpaCy...")
    for doc in doc_list:
        doc["spacy_doc"] = nlp(doc["text"])

    matches = []
    for doc in doc_list:
        matches.append(matcher(doc["spacy_doc"]))

    diets = []
    for a, ms in zip(doc_list, matches):
        for m in ms:
            _, _, end = m
            diets.append(a["spacy_doc"][end-1].text.lower())

    p = re.compile(r'feed \w+|feeds \w+')
    for d in doc_list:
        m = p.findall(str(d))
        if m:
            t = m[0].split(' ')[-1]
            diets.append(t.lower())

    return Counter(diets).most_common()
    # Output example:
    #return [("grass", 10), ("fish", 3)]
