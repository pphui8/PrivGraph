"""
based on the formal output, this is the final step before construct PrivGraph
"""
import argparse
import json
import os
import spacy
import yaml
from modules.text_splitter.text_splitter import Reddit_Splitter
from modules.named_entity_recognition.NER import NER
from modules.dependency_praser.dependency_praser import Dependency_parser
import modules.coreference_resolution.coreference_resolution as coref
from tqdm import tqdm
# import modules.annotators.owns.own as owns

class IntermediateGraph:
    def __init__(self):
        self.entities= []

    def add_entity(self, entity):
        self.entities.append(entity)

class Extractor:
    """
    input: segmented text
    output: intermediate output for constructing PrivGraph
    """
    def __init__(self, args):
        self.args = args
        self._init_PII_map()
        self.nlp = NER(args.NER_model_file, args.regex_pattern_file)
        with open(args.regex_pattern_file, "r", encoding='UTF8') as f:
            self.pattern_dict = yaml.safe_load(f)
        # with open(args.owns_verb_patterns_file, "r", encoding='UTF8') as f:
        #     self.owns_verb_patterns = yaml.safe_load(f)
        # self.onws_annotator = owns.owns_annotator(self.args.owns_verb_patterns_file)
        self.coref_annotator = coref.Coreference_reslution(self.args.device)
        self.dependency_parser = None
        self.graphs: list[IntermediateGraph] = []

    def _init_PII_map(self):
        """
        0: unique identifier
        1: non-unique identifier
        """
        self.PII_map = {
            "name": 0,
            "date_of_birth": 1,
            "gender": 1,
            "marital_status": 1,
            "nationality": 1,
            "age": 1,
            "home_address": 1,
            "email_address": 1,
            "phone_number": 1,
            "identify_number": 0,
            "social_security_number": 0,
            "passport_number": 0,
            "driver_license_ID": 0,
            "tax_identification_ID": 0,
            "student_ID": 0,
            "GPS_coordinates": 1,
            "work_place": 1,
            "travel_history": 1,
            "zip_code": 1,
            "IP_address": 1,
            "mac_address": 1,
            "cookies": 1,
            "usernames": 1,
            "blood_type": 0,
            "illness_symptoms": 1,
            "medical_diagnosis": 1,
            "religious_beliefs": 1,
            "political_opinions": 1,
            "education_background":1, 
            "employment_history": 1,
            "financial_information": 1,
            "cultural_affiliation": 1,  # wrong spell in the NLP model, remember to fix it.
        }

    def extract(self, text):
        """
        Extract entities and annotate them
        Args:
            text: segmented text
        Returns:
            result: intermediate output for constructing PrivGraph
        """
        self.graphs: list[IntermediateGraph] = []
        self.dependency_parser = Dependency_parser(text)
        self.entities = self._extract_entities(text)
        # self.owns_result, self.coref_result = self._annotate(text)
        self.coref_result = self._annotate(text)
        self._construct_intermediate_output()
        return self.graphs


    def _extract_entities(self, text):
        # return self.nlp.NER(text).ents
        ents = self.nlp.NER(text).ents
        for ent in ents:
            if ent.label == 'LOAN' or ent.label == 'INCOME' or ent.label == 'STOCKS':
                ent.label = "financial_information"
        return ents

    def _annotate(self, text) -> tuple:
        # 2. Annotate entities
        # 2.1. owns Annotator
        # owns_result = self.onws_annotator.annotate(text)
        # print("owns_result", owns_result)

        # 2.2. Coreference resolution
        coref_result = self.coref_annotator.resolute(text)
        # print("coref_result", coref_result)
        return coref_result
    
    def _construct_intermediate_output(self):
        """
        For each identified entities:
        """
        for entity in self.entities:
            entity_type = entity.label_.lower()
            sub = self.dependency_parser.find_subject_word(entity.start)
            if entity_type not in self.PII_map:
                continue
            # if entity is a unique identifier
            # looking at the existing graph, check if there is any redundant information
            elif self.PII_map[entity_type] == 0:
                # can find the corresponding individual graph
                is_found = False
                for graph in self.graphs:
                    for existing_entity in graph.entities:
                        # if the entity already exists in the graph
                        if existing_entity.start == entity.start:
                            graph.add_entity(entity)
                            is_found = True
                if not is_found:
                    # try its subject
                    if sub and sub.start != entity.start:
                        # find the corresponding entity in the graph
                        is_found = self._add_entity_by_subject(entity, sub)
                    # still not found, create a new graph
                    if not is_found:
                        new_graph = IntermediateGraph()
                        new_graph.add_entity(entity)
                        self.graphs.append(new_graph)
            # if entity is a non-unique identifier
            else:
                # print(f"found non-unique identifier {entity.text}")
                if sub:
                    is_found = self._add_entity_by_subject(entity, sub)
                # if the subject is not found, find the nearest unique identifier
                if not sub or not is_found:
                    nearest_ent = self._find_nearest_unique_identifier(entity)
                    if nearest_ent:
                        self._add_entity_by_subject(entity, nearest_ent)

    def _find_nearest_unique_identifier(self, entity):
        nearest_ent = None
        min_distance = float('inf')
        
        for candidate in self.entities:
            # Skip the entity itself if it's in the list
            if candidate == entity or self.PII_map.get(candidate.label_.lower(), 0) == 1:
                continue
            
            # Check if the candidate appears before the entity
            if candidate.start < entity.start:
                # Calculate the distance between the start token of the given entity and the candidate
                distance = entity.start - candidate.start
                
                # Update if we found a closer entity before the current entity
                if distance < min_distance:
                    min_distance = distance
                    nearest_ent = candidate
                    
        return nearest_ent
    
    def _add_entity_by_subject(self, entity, subject) -> bool:
        """
        first find the subject in the existing graph
        if not found, try identify the reference of the subject
        if still not found, add to nearest unique identifier 
        """
        # print(f"try to add {entity.text} with subject {subject.text}")
        is_found = False
        if entity.start != subject.start:
            for graph in self.graphs:
                for existing_entity in graph.entities:
                    if existing_entity.start == subject.start:
                        graph.add_entity(entity)
                        is_found = True
                        return is_found
        if not is_found:
            # print(f"failed to find the existing entity for {subject.text} in the existing graph, try to identify the reference of the subject")
            # print(f"start of the subject: {subject.start}")
            # identify the reference of the subject
            reference_start = None
            for coref in self.coref_result:
                if coref[3] == subject.start:
                    # record the reference start
                    reference_start = coref[1]
                    # print(f"found reference {coref[0]} for {subject.text}")
                    break
            if reference_start:
                for graph in self.graphs:
                    for existing_entity in graph.entities:
                        if existing_entity.start == reference_start:
                            graph.add_entity(entity)
                            is_found = True
                            break
        # print(f"add {entity.text} with subject {subject.text} is found: {is_found}\n")
        return is_found

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", type=str, default="cuda:0")
    # target text file
    parser.add_argument('--target_txt_file', type=str, default="./datasets/test.txt")
    # for NER
    parser.add_argument('--NER_model_file', type=str, default='./modules/named_entity_recognition/output/model-best')
    # for regex
    parser.add_argument('--regex_pattern_file', type=str, default='./modules/output/regex_pattern.jsonl')
    # # for owns annotator
    # parser.add_argument('--owns_verb_patterns_file', type=str, default='./modules/annotators/owns/verb_patterns.yml')
    parser.add_argument('--output_file', type=str, default='./output/intermediate_output.jsonl')
    args = parser.parse_args()

    # read target text
    print("Loading target text from: ", args.target_txt_file)
    with open(args.target_txt_file, "r", encoding='UTF8') as f:
        raw_data = f.read()

    # split text based on the semantic boundary
    # assume here we split based on Reddit conversation
    splitter = Reddit_Splitter()
    res = splitter.split(raw_data)
    
    print(f"found {len(res)} records")

    # extract
    extractor = Extractor(args=args)

    graphs_lists = []
    for index in tqdm(range(len(res))):
        if index == 0:
            continue
        text = res[index]
        graphs = extractor.extract(text)
        graphs_list = []
        
        for graph in graphs:
            graph_dict = {}
            for index, entity in enumerate(graph.entities):
                entity_dict = {
                    "text": entity.text,
                    "label": entity.label_,
                    "start": entity.start,
                    "end": entity.end
                }
                graph_dict[str(index)] = entity_dict
            graphs_list.append(graph_dict)
        graphs_lists.append(graphs_list)
    
    with open(args.output_file, 'w') as f:
        json.dump(graphs_lists, f, indent=4)
            
    print("Intermediate output is saved at: ", args.output_file)

    # text = res[5]
    # graphs = extractor.extract(text)

    # print("Graphs length: ", len(graphs))
    # for graph in graphs:
    #     print("< graph >:")
    #     for entity in graph.entities:
    #         print(entity.label_, entity.text, entity.start, entity.end)
    #         continue