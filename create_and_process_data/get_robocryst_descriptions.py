from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.io.cif import CifWriter, CifFile
import pymatgen
from pymatgen.core.structure import IStructure
from pymatgen.ext.matproj import MPRester
import csv
import os
import json
import random


# with open("/global/cfs/projectdirs/m3641/Shared/Materials_datasets/MP_data_latest/generate_scripts/mp.2018.6.1.json") as f:
    #structure_data = {i["material_id"]: i["structure"] for i in json.load(f)}
    # data = json.load(f)

API_KEY = 'D9q8LkJ5GoCCm4lQeaW93id3aH32p07r'

with MPRester(API_KEY) as m:
    data = m.summary.search(fields=['material_id', 'formation_energy_per_atom'])
    dataset = []
    used_ids = []
    for material in data:
        if material.formation_energy_per_atom != None:
            # 'get_data_by_id' is deprecated but the preferred 'search' causes an internal error
            description = m.materials.robocrys.get_data_by_id(material.material_id)
            if len(dataset) == 2000:
                break
            message_id_question = random.randint(1,1000000)
            message_id_answer = random.randint(1,1000000)
            try:
                structure_name = m.materials.get_structure_by_material_id(material.material_id).composition
                question_data_point = {'message_id': message_id_question, 'parent_id': None, 'text': f'Describe the material {str(structure_name)}', 'material_id': material.material_id}
                answer_data_point = {'message_id': message_id_answer, 'parent_id': message_id_question, 'text': description.description, 'material_id': material.material_id}
                dataset.append(question_data_point)
                dataset.append(answer_data_point)
            except: 
                print(material)
        else: 
            print('no form e')
    with open('../data/raw_robocryst_data_2000.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=['message_id', 'parent_id', 'text', 'material_id'])
        writer.writeheader()
        writer.writerows(dataset)
