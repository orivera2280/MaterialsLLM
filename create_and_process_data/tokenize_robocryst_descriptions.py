from transformers import AutoTokenizer, AutoModelForCausalLM
import csv

def tokenize(data):
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf", token='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')
    # tokenizer = tokenizer.train_new_from_iterator(iter(data), 150)
    tokenized_data = tokenizer.tokenize(data)
    tokenized_data = tokenizer.convert_tokens_to_ids(tokenized_data)
    return(tokenized_data)

data = []
with open('../data/raw_robocryst_data_2000.csv', 'r') as file:
     reader = csv.DictReader(file)
     for row in reader:
        data.append({'id': row['material_id'], 'description': row['text']})

tokenized_descriptions = [tokenize(i['description']) for i in data]

data_final = []
for i in range(len(data)):
    if i % 2 != 0:
        print(data[i])
        data_final.append({'id': data[i]['id'], 'tokenized_description': tokenized_descriptions[i]})

with open('/global/cfs/projectdirs/m3641/Oscar/MaterialsLLM2/data/tokenized_robocryst_descriptions_1000.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=['id', 'tokenized_description'])
    writer.writeheader()
    writer.writerows(data_final)
