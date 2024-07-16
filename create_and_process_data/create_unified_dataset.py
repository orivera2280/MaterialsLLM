import torch
import ast
import csv
import os

gnn_data = []
with open('/global/cfs/projectdirs/m3641/Oscar/MaterialsLLM2/data/gnn_embeddings_1000.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        gnn_data.append(row)

# gnn_data = torch.load('/global/cfs/projectdirs/m3641/Oscar/MaterialsLLM2/data/gnn_embeddings.pt')
# gnn_data = gnn_data[:1000]

robocryst_data = []
with open('/global/cfs/projectdirs/m3641/Oscar/MaterialsLLM2/data/tokenized_robocryst_descriptions_1000.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        robocryst_data.append(row)

unified_dataset = []

# for robocryst, gnn in zip(robocryst_data, gnn_data):

# unified_dataset.append({'label': robocryst, 'data': gnn.tolist()})
print(len(robocryst_data), len(gnn_data))
for r in robocryst_data:
    for n, g in enumerate(gnn_data):
        if r['id'][3:] == ast.literal_eval(g['id'])[0]:
            unified_dataset.append({'label': r['tokenized_description'], 'data': g['emb']})
            gnn_data.pop(n)

with open('../data/unified_dataset_1000.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=['label', 'data'])
    writer.writeheader()
    writer.writerows(unified_dataset)
