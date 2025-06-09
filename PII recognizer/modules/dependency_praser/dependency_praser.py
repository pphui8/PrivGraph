import re
import spacy
from spacy.matcher import Matcher

class Dependency_parser:
    def __init__(self, text):
        self.nlp = spacy.load("en_core_web_trf")
        self.doc = self.nlp(text)

    def find_subject_word(self, start_index):
        """
        Find the subject or subject-like entity related to the token at the given start index in the doc.
        """
        # Get the token based on the start index
        token = self.doc[start_index]

        # Traverse up the dependency tree to find the root or the verb linked to the token
        while token.dep_ != "ROOT" and token.head != token:
            token = token.head

            # Check if we find a subject-like token before finding a verb
            if token.dep_ in {"nsubj", "nsubjpass", "csubj", "csubjpass"}:
                # Try to find an entity that matches this token
                for entity in self.doc.ents:
                    if token in entity:
                        return entity
                return self.doc[token.i:token.i + 1]

            # If a verb is found, continue with the logic to find the subject of the verb
            if token.pos_ == "VERB":
                subject_token = None
                for child in token.children:
                    if child.dep_ in {"nsubj", "nsubjpass", "csubj", "csubjpass"}:  # Consider different types of subjects
                        subject_token = child
                        break

                if subject_token:
                    # Try to find an entity that matches this token
                    for entity in self.doc.ents:
                        if subject_token in entity:
                            return entity
                    return self.doc[subject_token.i:subject_token.i + 1]
            # Handle situations where the token is an attribute, modifier, or clausal modifier
            elif token.dep_ in {"attr", "nmod", "acl"}:
                for entity in self.doc.ents:
                    if token in entity:
                        return entity
                return self.doc[token.i:token.i + 1]

            # Additional handling for copula ("is") sentences
            if token.dep_ == "ROOT" and token.head == token and token.pos_ == "AUX":
                for child in token.children:
                    if child.dep_ in {"nsubj", "nsubjpass", "csubj", "csubjpass"}:
                        subject_token = child
                        # Return the entity if available
                        for entity in self.doc.ents:
                            if subject_token in entity:
                                return entity
                        return self.doc[subject_token.i:subject_token.i + 1]

        return None


if __name__ == "__main__":
    # Example text
    text = "Obama is the president of the United States."
    dependency_parser = Dependency_parser(text)
    nlp = spacy.load("en_core_web_sm")
    # Add the EntityRuler to the pipeline
    ruler = nlp.add_pipe("entity_ruler")
    patterns = [
        {"label": "ROLE", "pattern": "president"}
    ]
    ruler.add_patterns(patterns)

    # Add patterns to the ruler
    
    doc = nlp(text)
    for ent in doc.ents:
        print(ent.text, ent.label_, ent.start, ent.end)
        # sub = dependency_parser.find_subject_word(ent.start)
        # if sub:
        #     print(f"Subject for {ent.text}: {sub.text}")
        # else:
        #     print(f"No subject found for {ent.text}")