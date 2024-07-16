from pymatgen.ext.matproj import MPRester
from pymatgen.io.cif import CifWriter
import csv
import sys
import os
import ase
from ase import io, Atoms
from ase.db import connect
from pymatgen.io.ase import AseAtomsAdaptor
import json

###need 2 files: csv containing materials project IDs and atom_init.json (generic)

###get API key from materials project login dashboard online
API_KEY='D9q8LkJ5GoCCm4lQeaW93id3aH32p07r'
mpr = MPRester(API_KEY)

# id_list = []
# for i in range(1,1000):
    # id_list.append(f'mp-{i}')

data = mpr.summary.search(fields=["material_id", "task_id", "band_gap", "energy_per_atom", "formation_energy_per_atom", "structure"])
print(len(data), data[0])

adaptor = AseAtomsAdaptor()

#os.system('rm -rf ../raw')
#os.mkdir('../raw')

data_list=[]
for i in range(0, len(data)):
    # try:
        
    structure_id = data[i].material_id
    ase_crystal = adaptor.get_atoms(data[i].structure)   
    positions = ase_crystal.get_positions()
    cell = ase_crystal.get_cell()
    atomic_numbers = ase_crystal.get_atomic_numbers() 
    formation_energy = data[i].formation_energy_per_atom
    band_gap = data[i].band_gap
    energy = data[i].energy_per_atom
    data_dict = {'structure_id': structure_id[3:], 'positions' : positions.tolist(), 'cell' : cell.tolist(), 'atomic_numbers' : atomic_numbers.tolist(), 'energy' : energy, 'y' : formation_energy, 'band_gap' : band_gap, 'formation_energy' : formation_energy}
    if formation_energy != None:
        data_list.append(data_dict)

    # except Exception:
        # print(Exception)

with open('../data/data_for_gnn.json', 'w') as f:
    json.dump(data_list , f)
