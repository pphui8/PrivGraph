## steps for preparing the dataset
1. prepare all the entity datasets and put them into the correspond folder, you can refer the `make_dataset.py`, line 68.

2. run `python expand_template.py` to expand the template

3. run `python make_dataset.py` to generate the dataset

| final output would be `training_data.json` around `13.4GB`