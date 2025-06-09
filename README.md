# Graph_privacy

# PrivGraph is a tool to detect aggregation of PII in dataset.

Our paper has been accepted by QRS 2025.

## installaion

1. use conda to create a new environment
```bash
conda create -n PrivGraph python=3.11.5
```

2. install all the required packages
```bash
pip install -r requirements.txt
```


### Run the following command to build PrivGraph
1. Prepare regex pattern for regular expression
```bash
cd PII recognizer/modules/named_entity_recognition/regular_expression
python pattern_to_json.py
```

2. directly run ./PII recognizer/extract_PII.py
```bash
cd Textual_data
python extract_PII.py
```

3. run the following command to build data type
```bash
cd PrivGraph_constructor
python DataType.py
```

4. Run the following command to build PrivGraph
```bash
cd ..
cd PrivGraph_constructor
python Textual.py
```

### train the NER model
1. run the following command to train the NER model
```bash
cd Textual_data/modules/named_entity_recognition
python -m spacy init fill-config base_config.cfg config.cfg

python -m spacy train config.cfg --output ./output --paths.train ./train.spacy --paths.dev ./validate.spacy | tee output.txt
```

### Known issues
1. the NER model was trained using Ubuntu 20.04, load the model on windows may cause some issues.
