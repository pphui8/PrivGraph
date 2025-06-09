import json
import random
import re

def load_file(filepath):
    with open(filepath, 'r', encoding='UTF8') as file:
        return [line.strip() for line in file.readlines()]

def generate_date_of_birth():
    monthes = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    day = random.randint(1, 31)
    # random select month representation "English" or "number"
    month = random.choice([random.randint(1, 12), random.choice(monthes)])
    year = random.randint(1900, 2024)

    # condition for year only
    if year / 13 == 0:
        return str(year)

    # random select date format
    # if month is represented by number, the date format should be "dd/mm/yyyy" or "mm/dd/yyyy" or "yyyy/mm/dd"
    if type(month) == int:
        date_format = random.choice(["dd/mm/yyyy", "dd-mm-yyyy", "dd.mm.yyyy", "mm/dd/yyyy", "mm-dd-yyyy", "mm.dd.yyyy", "yyyy/mm/dd", "yyyy-mm-dd", "yyyy.mm.dd"])
        # replace dd
        date_format = date_format.replace("dd", str(day))
        # replace mm
        date_format = date_format.replace("mm", str(month))
        # replace yyyy
        date_format = date_format.replace("yyyy", str(year))
        return date_format
    else:
        date_format = random.choice(["dd month yyyy", "dd month, yyyy", "month dd, yyyy", "month dd yyyy", "month dd yyyy", "month dd, yyyy", "month yyyy", "yyyy month dd", "yyyy month dd", "yyyy month, dd", "yyyy month dd", "yyyy month, dd", "month yyyy", "yyyy month"])
        # replace dd
        date_format = date_format.replace("dd", str(day) + 'th')
        # replace month
        date_format = date_format.replace("month", month)
        # replace yyyy
        date_format = date_format.replace("yyyy", str(year))
        return date_format

def generate_blood_type():
    blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    return random.choice(blood_types)

def generate_financial_info():
    amount = random.randint(0, 10000000)
    carrency_denote = random.choice(["$", "€", "¥", "₩", "dollar", "euro", "yen", "won", "yuan"])
    return str(amount) + carrency_denote

def correctness_check():
    for sentence in template_sentences:
            for _ in range(100):
                current_sentence = sentence
                entities = []
                for entity_name, entity_list in replace_map.items():
                    for entity in entity_list:
                        if entity_name in current_sentence:
                            entity_label = "%" + entity_name + "%"
                            candidate_entity = random.choice(entity_list)
                            current_sentence = current_sentence.replace(entity_label, candidate_entity, 1)
                            start = current_sentence.find(candidate_entity)
                            end = start + len(candidate_entity)
                            entities.append({'start': start, 'end': end, 'label': entity_name})

def is_english(text):
    return bool(re.match(r'^[a-zA-Z0-9\s\W]+$', text))

if __name__ == '__main__':
    # Example: Define the file paths for the template and multiple entity list files
    template_file = 'expanded_template.txt'
    entity_files = {
        'NAME': './1_names/names.txt',
        'NATIONALITY': './2_nationality/country_names.txt',
        'HOME_ADDRESS': './3_home_address/city_names.txt',
        'WORK_PLACE': ['./4_work_place/company_names.txt', './4_work_place/universities.txt', './4_work_place/city_names.txt'],
        'TRAVEL_HISTORY': ['./5_travel_history/country_names.txt', './5_travel_history/city_names.txt'],
        'USERNAMES': './6_usernames/usernames.txt',
        'ILLNESS_SYMPTOMS': './7_health_records/symptoms.txt',
        'MEDICAL_DIAGNOSIS': './7_health_records/illness.txt',
        'RELIGIOUS_BELIEFS': './8_religious_belifs/religious.txt',
        'POLITICAL_OPINIONS': './9_political_opinions/party_names.txt',
        'EMPLOYMENT_HISTORY': './10_employment_history/company_names.txt',
        'EDUCATION_BACKGROUND': ['./11_education_background/universities.txt', './11_education_background/school_names.txt'],
        'CULTURAL_AFFILIATION': './12_cultural_affiliation/ethnic.txt'
    }

    # Load template sentences
    template_sentences = load_file(template_file)

    names = load_file(entity_files['NAME'])
    # remove non-english names
    names = [name for name in names if is_english(name)]
    if len(names) > 10000:
        names = random.sample(names, 10000)
    print("got ", len(names), " names records")
    print("example names: ", names[random.randint(1, 100)])

    date_of_births = [generate_date_of_birth() for _ in range(10000)]
    print("got ", len(date_of_births), " date of birth records")
    print("example date of birth: ", date_of_births[random.randint(1, 100)])

    country_names = load_file(entity_files['NATIONALITY'])
    country_names = [country for country in country_names if is_english(country)]
    if len(country_names) > 10000:
        country_names = random.sample(country_names, 10000)
    print("got ", len(country_names), " country names records")
    print("example country names: ", country_names[random.randint(1, 100)])

    home_address = load_file(entity_files['HOME_ADDRESS'])
    home_address = [address for address in home_address if is_english(address)]
    if len(home_address) > 10000:
        home_address = random.sample(home_address, 10000)
    print("got ", len(home_address), " home address records")
    print("example home address: ", home_address[random.randint(1, 100)])
    
    work_place = []
    for file_path in entity_files['WORK_PLACE']:
        work_place += load_file(file_path)
    work_place = [work for work in work_place if is_english(work)]
    if len(work_place) > 10000:
        work_place = random.sample(work_place, 10000)
    print("got ", len(work_place), " work place records")
    print("example work place: ", work_place[random.randint(1, 100)])

    travel_history = []
    for file_path in entity_files['TRAVEL_HISTORY']:
        travel_history += load_file(file_path)
    travel_history = [travel for travel in travel_history if is_english(travel)]
    if len(travel_history) > 10000:
        travel_history = random.sample(travel_history, 10000)
    print("got ", len(travel_history), " travel history records")
    print("example travel history: ", travel_history[random.randint(1, 100)])

    usernames = load_file(entity_files['USERNAMES'])
    usernames = [username for username in usernames if is_english(username)]
    if len(usernames) > 10000:
        usernames = random.sample(usernames, 10000)
    print("got ", len(usernames), " usernames records")
    print("example usernames: ", usernames[random.randint(1, 100)])

    blood_types = [generate_blood_type() for _ in range(10000)]
    print("got ", len(blood_types), " blood types records")
    print("example blood types: ", blood_types[random.randint(1, 100)])

    illness_symptoms = load_file(entity_files['ILLNESS_SYMPTOMS'])
    illness_symptoms = [symptom for symptom in illness_symptoms if is_english(symptom)]
    if len(illness_symptoms) > 10000:
        illness_symptoms = random.sample(illness_symptoms, 10000)
    print("got ", len(illness_symptoms), " illness symptoms records")
    print("example illness symptoms: ", illness_symptoms[random.randint(1, 100)])

    medical_diagnosis = load_file(entity_files['MEDICAL_DIAGNOSIS'])
    medical_diagnosis = [diagnosis for diagnosis in medical_diagnosis if is_english(diagnosis)]
    if len(medical_diagnosis) > 10000:
        medical_diagnosis = random.sample(medical_diagnosis, 10000)
    print("got ", len(medical_diagnosis), " medical diagnosis records")
    print("example medical diagnosis: ", medical_diagnosis[random.randint(1, 100)])

    religious_beliefs = load_file(entity_files['RELIGIOUS_BELIEFS'])
    religious_beliefs = [belief for belief in religious_beliefs if is_english(belief)]
    if len(religious_beliefs) > 10000:
        religious_beliefs = random.sample(religious_beliefs, 10000)
    print("got ", len(religious_beliefs), " religious beliefs records")
    print("example religious beliefs: ", religious_beliefs[random.randint(1, 100)])

    political_opinions = load_file(entity_files['POLITICAL_OPINIONS'])
    political_opinions = [opinion for opinion in political_opinions if is_english(opinion)]
    if len(political_opinions) > 10000:
        political_opinions = random.sample(political_opinions, 10000)
    print("got ", len(political_opinions), " political opinions records")
    print("example political opinions: ", political_opinions[random.randint(1, 100)])

    employment_history = load_file(entity_files['EMPLOYMENT_HISTORY'])
    employment_history = [employment for employment in employment_history if is_english(employment)]
    if len(employment_history) > 10000:
        employment_history = random.sample(employment_history, 10000)
    print("got ", len(employment_history), " employment history records")
    print("example employment history: ", employment_history[random.randint(1, 100)])

    education_background = []
    for file_path in entity_files['EDUCATION_BACKGROUND']:
        education_background += load_file(file_path)
    education_background = [education for education in education_background if is_english(education)]
    if len(education_background) > 10000:
        education_background = random.sample(education_background, 10000)
    print("got ", len(education_background), " education background records")
    print("example education background: ", education_background[random.randint(1, 100)])

    financial_info = [generate_financial_info() for _ in range(10000)]
    print("got ", len(financial_info), " financial info records")
    print("example financial info: ", financial_info[random.randint(1, 100)])

    cultural_affiliation = load_file(entity_files['CULTURAL_AFFILIATION'])
    cultural_affiliation = [affiliation for affiliation in cultural_affiliation if is_english(affiliation)]
    if len(cultural_affiliation) > 10000:
        cultural_affiliation = random.sample(cultural_affiliation, 10000)
    print("got ", len(cultural_affiliation), " cultural affiliation records")
    print("example cultural affiliation: ", cultural_affiliation[random.randint(1, 100)])

    replace_map = {
        'NAME': names,
        'DATE_OF_BIRTH': date_of_births,
        'NATIONALITY': country_names,
        'HOME_ADDRESS': home_address,
        'WORK_PLACE': work_place,
        'TRAVEL_HISTORY': travel_history,
        'USERNAMES': usernames,
        'BLOOD_TYPE': blood_types,
        'ILLNESS_SYMPTOMS': illness_symptoms,
        'MEDICAL_DIAGNOSIS': medical_diagnosis,
        'RELIGIOUS_BELIEFS': religious_beliefs,
        'POLITICAL_OPINIONS': political_opinions,
        'EMPLOYMENT_HISTORY': employment_history,
        'EDUCATION_BACKGROUND': education_background,
        # 'FINANCIAL_INFO'
        'LOAN': financial_info,
        'INCOME': financial_info,
        'STOCKS': financial_info,
        'CULTURAL_AFFILIATION': cultural_affiliation
    }
    print("found ", len(template_sentences), " template sentences")

    # For each template sentence, replace the placeholders with the corresponding entities, memorize the location of the entities, and save the result as a JSON file
    # output: [('The F15 aircraft uses a lot of fuel', {'entities': [(4, 7, 'aircraft')]}), ('The F15 aircraft uses a lot of fuel', {'entities': [(4, 7, 'aircraft')]})]
    # each template generate 100 records
    # entities in sentence are formatted as %ENTITY_NAME%
    
    # training data
    # each template generate 10 records
    templeate_multiplier = 8
    output_file = 'training_data.json'
    
    print(len(template_sentences) * templeate_multiplier, " records will be generated")
    print("Generating training data...")
    current_progress = 0
    target_progress = len(template_sentences) * templeate_multiplier
    with open(output_file, 'w', encoding='UTF8') as file:
        file.write('[\n')
        for sentence in template_sentences:
            for _ in range(templeate_multiplier):
                current_sentence = sentence
                entities = []
                for entity_name, entity_list in replace_map.items():
                    for entity in entity_list:
                        entity_label = "%" + entity_name + "%"
                        if entity_label in current_sentence:
                            candidate_entity = random.choice(entity_list)
                            current_sentence = current_sentence.replace(entity_label, candidate_entity, 1)
                            start = current_sentence.find(candidate_entity)
                            end = start + len(candidate_entity)
                            entities.append({'start': start, 'end': end, 'label': entity_name})
                json.dump({'text': current_sentence, 'entities': entities}, file, ensure_ascii=False)
                file.write(',\n')
                current_progress += 1
                if current_progress % 1000 == 0:
                    print(f"{current_progress}/{target_progress} records generated")
        # this is to remove the last comma
        file.write('{"text": "Marguerite Marie Chanvril, born 22th June 1992, I is a citizen of Eswatini", "entities": [{"start": 0, "end": 25, "label": "NAME"}, {"start": 32, "end": 46, "label": "DATE_OF_BIRTH"}, {"start": 66, "end": 74, "label": "NATIONALITY"}]}')
        file.write(']')
    
    print(f"Generated {current_progress} testing data")
    print(f"Testing data has been saved to {output_file}")

    # # testing data
    # templeate_multiplier = 1
    # output_file = 'testing_data.json'
    # print("Generating testing data...")
    # print(len(template_sentences) * templeate_multiplier, " records will be generated")
    # current_progress = 0
    # target_progress = len(template_sentences) * 10
    # with open(output_file, 'w', encoding='UTF8') as file:
    #     file.write('[\n')
    #     for sentence in template_sentences:
    #         for _ in range(templeate_multiplier):
    #             current_sentence = sentence
    #             entities = []
    #             for entity_name, entity_list in replace_map.items():
    #                 for entity in entity_list:
    #                     entity_label = "%" + entity_name + "%"
    #                     if entity_label in current_sentence:
    #                         candidate_entity = random.choice(entity_list)
    #                         current_sentence = current_sentence.replace(entity_label, candidate_entity, 1)
    #                         start = current_sentence.find(candidate_entity)
    #                         end = start + len(candidate_entity)
    #                         entities.append({'start': start, 'end': end, 'label': entity_name})
    #             json.dump({'text': current_sentence, 'entities': entities}, file, ensure_ascii=False)
    #             file.write(',\n')
    #             current_progress += 1
    #             if current_progress % 1000 == 0:
    #                 print(f"{current_progress}/{target_progress} records generated")
    #     # this is to remove the last comma
    #     file.write('{"text": "Marguerite Marie Chanvril, born 22th June 1992, I is a citizen of Eswatini", "entities": [{"start": 0, "end": 25, "label": "NAME"}, {"start": 32, "end": 46, "label": "DATE_OF_BIRTH"}, {"start": 66, "end": 74, "label": "NATIONALITY"}]}')
    #     file.write(']')
        

    # correctness_check()

    print(f"Generated {current_progress} testing data")
    print(f"Validate data has been saved to {output_file}")

    # ### validate data
    # templeate_multiplier = 1
    # output_file = 'validate_data.json'
    # print("Generating validate data...")
    # print(len(template_sentences) * templeate_multiplier, " records will be generated")
    # current_progress = 0
    # target_progress = len(template_sentences) * templeate_multiplier
    # with open(output_file, 'w', encoding='UTF8') as file:
    #     file.write('[\n')
    #     for sentence in template_sentences:
    #         for _ in range(templeate_multiplier):
    #             current_sentence = sentence
    #             entities = []
    #             for entity_name, entity_list in replace_map.items():
    #                 for entity in entity_list:
    #                     entity_label = "%" + entity_name + "%"
    #                     if entity_label in current_sentence:
    #                         candidate_entity = random.choice(entity_list)
    #                         current_sentence = current_sentence.replace(entity_label, candidate_entity, 1)
    #                         start = current_sentence.find(candidate_entity)
    #                         end = start + len(candidate_entity)
    #                         entities.append({'start': start, 'end': end, 'label': entity_name})
    #             json.dump({'text': current_sentence, 'entities': entities}, file, ensure_ascii=False)
    #             file.write(',\n')
    #             current_progress += 1
    #             if current_progress % 1000 == 0:
    #                 print(f"{current_progress}/{target_progress} records generated")
    #     # this is to remove the last comma
    #     file.write('{"text": "Marguerite Marie Chanvril, born 22th June 1992, I is a citizen of Eswatini", "entities": [{"start": 0, "end": 25, "label": "NAME"}, {"start": 32, "end": 46, "label": "DATE_OF_BIRTH"}, {"start": 66, "end": 74, "label": "NATIONALITY"}]}')
    #     file.write(']')
        

    # # correctness_check()

    # print(f"Generated {current_progress} validate data")
    # print(f"Validate data has been saved to {output_file}")