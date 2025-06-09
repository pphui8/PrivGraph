import json
import spacy
import argparse
from abc import ABCMeta, abstractmethod

class Splitter(metaclass=ABCMeta):
    """
    Abstract base class for splitting raw text into segments.  
    Input: raw text  
    Output: segmented text
    """
    def __init__(self):
        self.texts = []

    @abstractmethod
    def split(self, raw_text) -> list:
        pass

class Reddit_Splitter(Splitter):
    """
    A concrete class inheriting from Splitter, designed to split Reddit conversations.
    """
    def __init__(self):
        super().__init__()

    def split(self, raw_text) -> list:
        conversation = ""
        for line in raw_text.split('\n'):
            # new conversation
            if line == '' or line == "[deleted]":
                continue
            elif line.startswith('Conversation ID'):
                self.texts.append(conversation)
                conversation = ""
            else:
                conversation += line + ' '
        return self.texts

class NER:
    """
    model_path: path to the model  
    regex_pattern_file: path to the regex pattern file
    """
    def __init__(self, model_path, regex_pattern_file):
        # self.nlp = spacy.load(model_path)
        self.nlp = spacy.load("en_core_web_trf")
        self.ruler = self.nlp.add_pipe("entity_ruler")
        with open(regex_pattern_file, "r", encoding='UTF8') as f:
            regex_patterns = json.load(f)
        self.ruler.add_patterns(regex_patterns)
    
    def NER(self, text):
        return self.nlp(text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', type=str, default='./output/model-best')
    parser.add_argument('--regex_pattern_file', type=str, default='../output/regex_pattern.jsonl')
    parser.add_argument('--test_txt_file', type=str, default="../../datasets/test.txt")
    args = parser.parse_args()

    # Test the model with some text
    with open(args.test_txt_file, 'r', encoding="UTF8") as f:
        text = f.read()
    Reddit_Splitter = Reddit_Splitter()
    test_cases = Reddit_Splitter.split(text)
    # print("test_cases: ", test_cases[1])

    nlp = NER(args.model_path, args.regex_pattern_file)
    results = []
    print("NER start:\n")
    doc = nlp.NER("Obama is the president of the United States. He was born in Hawaii. He is a good president. His wife is Michelle Obama. She is a lawyer. She is a good wife.")
    # doc = nlp.
    for ent in doc.ents:
        print(ent.text, ent.label_)






