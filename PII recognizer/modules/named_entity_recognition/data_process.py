import spacy
from spacy.tokens import DocBin
import json

if __name__ == '__main__':
    json_file_path = 'training_data.json'

    nlp = spacy.load("en_core_web_trf")
    db = DocBin()

    with open('training_data.json', 'r', encoding='UTF8') as file:
        data = json.load(file)
    # with open('testing_data.json', 'r', encoding='UTF8') as file:
    #     data = json.load(file)
    # with open('validate_data.json', 'r', encoding='UTF8') as file:
    #     data = json.load(file)
    
    print(f"Total items in the list: {len(data)}")

    records_num = 0
    emp_sen = 0
    entities_num = 0
    wrong_ents = 0
    for index, item in enumerate(data):
        text = item['text']
        entities = item['entities']
        ents = []
        doc = nlp.make_doc(text)
        for record in entities:
            start = record['start']
            end = record['end']
            label = record['label']
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is None:
                wrong_ents += 1
            else:
                ents.append(span)
                entities_num += 1
        try:
            if ents != []:
                doc.ents = ents
                db.add(doc)
                records_num += 1
            else:
                emp_sen += 1
        except:
            print(f"Error in index: {index}")

    db.to_disk("./train.spacy")
    # db.to_disk("./test.spacy")
    # db.to_disk("./validate.spacy")
    print("Total records added: ", records_num)
    print("Total entities added: ", entities_num)
    print("Total entities that wrong: ", wrong_ents)
    print("Total empty sentence: ", emp_sen)