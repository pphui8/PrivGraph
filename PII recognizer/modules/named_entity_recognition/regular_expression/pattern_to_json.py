"""
transfer regex pattern from yaml to jsonl file
"""

import argparse
import re
import yaml
import json


# def extract_from_text(text, pattern_dict) -> list:
#   """
#   Extract patterns from text
#   output: Entity, Start, End, Label
#   """
#   results = []

#   # Collect all: Entity,Start,End,Label
#   for key in pattern_dict.keys():
#     patterns = pattern_dict[key]
#     for pattern in patterns:
#       for match in re.finditer(pattern, text):
#         results.append((match.group(), match.start(), match.end(), key))
#   return results

# template = {
#     "label": "email",
#     "pattern": [
#         {"TEXT": {"REGEX": "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"}}
#     ]
# }

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--pattern_file', type=str, default='../../../datasets/PII patterns/pattern.yml')
  parser.add_argument('--output_file', type=str, default='../../output/regex_pattern.jsonl')
  args = parser.parse_args()

  # read pattern from pattern.yaml
  print("Loading pattern file from: ", args.pattern_file)
  with open(args.pattern_file, "r", encoding='UTF8') as f:
    pattern_dict = yaml.safe_load(f)

  spacy_patterns = []
  for key in pattern_dict.keys():
    patterns = pattern_dict[key]
    key = key.upper()
    for pattern in patterns:
        # Modify the pattern to include [Xx] after \b for the first character
        modified_pattern = re.sub(r'\\b([a-zA-Z])', lambda m: r'\b[' + m.group(1).upper() + m.group(1).lower() + ']', pattern)
        # Create the spaCy pattern
        spacy_pattern = {
            "label": key,
            "pattern": [
                {"TEXT": {"REGEX": modified_pattern}}
            ]
        }
        spacy_patterns.append(spacy_pattern)

  # write to output file
  print("Writing pattern to: ", args.output_file)
  with open(args.output_file, "w", encoding='UTF8') as f:
    json.dump(spacy_patterns, f, indent=2)
  