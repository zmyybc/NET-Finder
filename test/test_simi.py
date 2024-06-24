from ase.io import read
from scipy.spatial.transform import Rotation
import numpy as np

from ase.build import niggli_reduce

def structures_are_similar(structure1, structure2, structure_diff_threshold=0.1):
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

    print(f'RMSD between structures: {rmsd}')
    return rmsd < structure_diff_threshold
# 读取两个 .vasp 文件
structure1 = read('../reaction_network_output/Product_13.vasp')
structure2 = read('../reaction_network_output/Product_14.vasp')

# 比较结构相似度
similar = structures_are_similar(structure1, structure2)

if similar:
    print('The two structures are similar')
else:
    print('The two structures are different')
