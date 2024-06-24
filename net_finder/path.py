import json
from ase.io import read, write

class ReactionPath:
    def __init__(self, structures=None, energies=None, ts_index=None):
        self.structures = structures
        self.energies = energies
        self.ts_index = ts_index

    @property
    def reactant(self):
        return self.structures[0]

    @property
    def product(self):
        return self.structures[-1]

    @property
    def transition_state(self):
        if self.ts_index is not None:
            return self.structures[self.ts_index]
        else:
            return None

    @property
    def reactant_energy(self):
        return self.energies[0]

    @property
    def product_energy(self):
        return self.energies[-1]

    @property
    def transition_state_energy(self):
        if self.ts_index is not None:
            return self.energies[self.ts_index]
        else:
            return None

    def to_dict(self):
        data = {
            'structures': [f'structure_{i}.vasp' for i in range(len(self.structures))],
            'energies': self.energies,
            'ts_index': self.ts_index
        }
        return data

    def save(self, directory):
        for i, structure in enumerate(self.structures):
            filename = f'structure_{i}.vasp'
            structure.write(f'{directory}/{filename}')
        
        data = self.to_dict()
        with open(f'{directory}/reaction_path.json', 'w') as f:
            json.dump(data, f)

    @classmethod
    def load(cls, directory):
        with open(f'{directory}/reaction_path.json', 'r') as f:
            data = json.load(f)
        
        structures = []
        for filename in data['structures']:
            structure = read(f'{directory}/{filename}')
            structures.append(structure)
        
        energies = data['energies']
        ts_index = data['ts_index']
        
        return cls(structures, energies, ts_index)
