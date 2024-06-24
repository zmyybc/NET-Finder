import os
import hashlib
import logging
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from ase.geometry import get_distances
from scipy.spatial.transform import Rotation
from .path import ReactionPath
from ase.build import niggli_reduce

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ReactionNetwork:
    def __init__(self, reaction_paths, energy_cutoff=None, structure_diff_threshold=0.1):
        self.reaction_paths = reaction_paths
        self.energy_cutoff = energy_cutoff
        self.structure_diff_threshold = structure_diff_threshold
        
        logger.info(f'Initializing ReactionNetwork with {len(reaction_paths)} reaction paths, energy cutoff: {energy_cutoff}, structure difference threshold: {structure_diff_threshold}')
        self.filtered_reaction_paths = self._filter_reaction_paths()
        logger.info(f'After filtering, {len(self.filtered_reaction_paths)} unique reaction paths remain')

    def _filter_reaction_paths(self):
        filtered_paths = []

        for path in self.reaction_paths:
            if self.energy_cutoff is None or (
                path.reactant_energy < self.energy_cutoff and
                path.product_energy < self.energy_cutoff
            ):
                is_unique = True
                for unique_path in filtered_paths:
                    if (
                        self._structures_are_similar(path.reactant, unique_path.reactant) and
                        self._structures_are_similar(path.product, unique_path.product) and
                        (
                            (path.transition_state is None and unique_path.transition_state is None) or
                            (path.transition_state is not None and unique_path.transition_state is not None and
                             self._structures_are_similar(path.transition_state, unique_path.transition_state))
                        )
                    ):
                        is_unique = False
                        logger.debug(f'Reaction path {path} is similar to {unique_path}, considered as duplicate')
                        break
                if is_unique:
                    filtered_paths.append(path)
                    logger.debug(f'Reaction path {path} is unique, added to filtered paths')

        return filtered_paths

    def _structures_are_similar(self, structure1, structure2):
        if len(structure1) != len(structure2):
            return False
        if structure1.get_chemical_symbols() != structure2.get_chemical_symbols():
            return False
    
        # 对结构应用 Niggli 约简
        niggli_reduce(structure1)
        niggli_reduce(structure2)
    
        # 计算结构之间的距离矩阵
        dist1 = structure1.get_all_distances(mic=True)
        dist2 = structure2.get_all_distances(mic=True)
    
        # 计算距离矩阵之间的均方根偏差 (RMSD)
        rmsd = np.sqrt(np.mean((dist1 - dist2)**2))
        logger.debug(f'RMSD between structures: {rmsd}')
        return rmsd < self.structure_diff_threshold

    def _get_path_id(self, path):
        reactant_id = self._get_structure_id(path.reactant)
        ts_id = self._get_structure_id(path.transition_state) if path.transition_state else None
        product_id = self._get_structure_id(path.product)
        path_id = (reactant_id, ts_id, product_id)
        logger.debug(f'Generated path ID: {path_id}')
        return path_id

    def _get_structure_id(self, structure):
        chemical_formula = structure.get_chemical_formula()
        positions = structure.positions.flatten()

        formula_bytes = chemical_formula.encode('utf-8')
        positions_bytes = positions.tobytes()

        hash_object = hashlib.sha256()
        hash_object.update(formula_bytes)
        hash_object.update(positions_bytes)
        hash_value = hash_object.hexdigest()

        logger.debug(f'Generated structure ID: {hash_value}')
        return hash_value

    def generate_graph(self, output_dir='reaction_network'):
       logger.info(f'Generating reaction network graph, output directory: {output_dir}')
   
       if not os.path.exists(output_dir):
           os.makedirs(output_dir)
   
       # 创建子目录用于存储反应路径信息
       paths_dir = os.path.join(output_dir, 'reaction_paths')
       os.makedirs(paths_dir, exist_ok=True)
   
       # 创建子目录用于存储不重复的物种
       species_dir = os.path.join(output_dir, 'unique_species')
       os.makedirs(species_dir, exist_ok=True)
   
       # 创建子目录用于存储不重复的过渡态
       ts_dir = os.path.join(output_dir, 'transition_states')
       os.makedirs(ts_dir, exist_ok=True)
   
       G = nx.Graph()
   
       # 收集所有物种和过渡态
       species = []
       transition_states = []
       for i, path in enumerate(self.filtered_reaction_paths):
           self._add_unique_species(species, path.reactant, path.reactant_energy)
           self._add_unique_species(species, path.product, path.product_energy)
           if path.transition_state is not None:
               self._add_unique_species(transition_states, path.transition_state, path.transition_state_energy)
   
           # 保存反应路径信息
           path_dir = os.path.join(paths_dir, f'path_{i}')
           os.makedirs(path_dir, exist_ok=True)
           path.reactant.write(os.path.join(path_dir, 'reactant.vasp'))
           path.product.write(os.path.join(path_dir, 'product.vasp'))
           if path.transition_state is not None:
               path.transition_state.write(os.path.join(path_dir, 'transition_state.vasp'))
           with open(os.path.join(path_dir, 'energies.txt'), 'w') as f:
               f.write(f'Reactant energy: {path.reactant_energy}\n')
               f.write(f'Product energy: {path.product_energy}\n')
               if path.transition_state is not None:
                   f.write(f'Transition state energy: {path.transition_state_energy}\n')
   
       # 添加物种节点
       for i, (structure, energy) in enumerate(species):
           node_name = f'Species_{i}'
           G.add_node(node_name, energy=energy, structure=structure, node_type='species')
           structure.write(os.path.join(species_dir, f'{node_name}.vasp'))
   
       # 添加过渡态节点
       for i, (structure, energy) in enumerate(transition_states):
           node_name = f'TS_{i}'
           G.add_node(node_name, energy=energy, structure=structure, node_type='transition_state')
           structure.write(os.path.join(ts_dir, f'{node_name}.vasp'))
   
       logger.info('Added all unique species and transition states as nodes')
   
       # 根据反应路径添加边
       for path in self.filtered_reaction_paths:
           reactant_node = None
           product_node = None
           ts_node = None
   
           for node_name, data in G.nodes(data=True):
               if data['node_type'] == 'species':
                   if self._structures_are_similar(data['structure'], path.reactant):
                       reactant_node = node_name
                   elif self._structures_are_similar(data['structure'], path.product):
                       product_node = node_name
               elif data['node_type'] == 'transition_state' and path.transition_state is not None:
                   if self._structures_are_similar(data['structure'], path.transition_state):
                       ts_node = node_name
   
           if reactant_node is not None and product_node is not None:
               if ts_node is not None:
                   G.add_edge(reactant_node, ts_node)
                   G.add_edge(ts_node, product_node)
               else:
                   G.add_edge(reactant_node, product_node)
   
       logger.info('Added edges based on reaction paths')
   
       # 使用 spring_layout 算法优化布局
       pos = nx.spring_layout(G, k=0.5, iterations=50)
   
       fig, ax = plt.subplots(figsize=(20, 20))
   
       node_labels = {n: f"{n}\nEnergy: {d['energy']:.2f}" for n, d in G.nodes(data=True)}
       nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=12, ax=ax)
   
       node_size = 1000
       species_nodes = [n for n, d in G.nodes(data=True) if d['node_type'] == 'species']
       ts_nodes = [n for n, d in G.nodes(data=True) if d['node_type'] == 'transition_state']
       nx.draw_networkx_nodes(G, pos, nodelist=species_nodes, node_color='lightblue', node_size=node_size, ax=ax)
       nx.draw_networkx_nodes(G, pos, nodelist=ts_nodes, node_color='red', node_shape='s', node_size=node_size, ax=ax)
       nx.draw_networkx_edges(G, pos, edge_color='black', ax=ax, alpha=0.7)
   
       plt.axis('off')
       plt.tight_layout()
       plt.savefig(os.path.join(output_dir, 'reaction_network.png'), dpi=300)
       plt.close()
   
       logger.info(f'Reaction network graph saved to {os.path.join(output_dir, "reaction_network.png")}')
       logger.info('All structures and energies saved to files')
   
    def _add_unique_species(self, species_list, structure, energy):
       for s, e in species_list:
           if self._structures_are_similar(s, structure):
               return
       species_list.append((structure, energy))