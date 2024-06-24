import os
from ase.io import read
from ase.calculators.emt import EMT
from net_finder.paths import TransitionStateSearch
from net_finder.net import ReactionNetwork
from ase.calculators.vasp import Vasp
# 读取初始结构
#initial_structures = [read('initial_1.vasp'), read('initial_2.vasp'), read('initial_3.vasp')]
from ase import Atoms
from ase.build import fcc111, add_adsorbate
# 设置计算器

# 指定initial目录的路径
initial_dir = "initial"

# 获取initial目录下所有的.vasp文件
vasp_files = [f for f in os.listdir(initial_dir) if f.endswith(".vasp")]

calc= {
  "calculator_imports": "from ase.calculators.vasp import Vasp",
  "calculator_setup": "calc = Vasp(xc='pbe', encut=400, icharg=1, ncore=32, kpts=(1, 1, 1), ismear=0, sigma=0.01, isym=0, ispin=2, nupdown=4, algo='fast', gamma=True, nsw=0, lwave=True, lcharg=True, nelm=200, ediff=0.0001)"
 
}
# 初始化一个空列表来存储读取的结构
structures = []

# 遍历每个.vasp文件并读取结构
for vasp_file in vasp_files:
    file_path = os.path.join(initial_dir, vasp_file)
    structure = read(file_path)
    structures.append(structure)

# 设置Dimer参数
dimer_params = {
    'displacement_method': 'gauss',
    'displacement_radius': 2.0,
    'dimer_separation': 0.01,
}
slurm_params = {
    'nodes': 1,  # 请求的节点数
    "account": 'che190010',
    "ntasks": 128,
    'time': '12:00:00',  # 请求的最大运行时间 (HH:MM:SS)
    'partition': 'shared',  # 请求的分区 (队列)
    
}
# 创建TransitionStateSearch对象并运行
ts_search = TransitionStateSearch(structures, calc, dimer_params, output_dir='/anvil/scratch/x-wang3/yinbc/test_net/output_dim4', run_mode='slurm',slurm_params=slurm_params)
ts_search.run(fmax=0.05, steps=100)

# 收集反应路径
reaction_paths = ts_search.collect_reaction_paths()

# 创建ReactionNetwork对象并生成图形
energy_cutoff = -22.5
network = ReactionNetwork(reaction_paths, energy_cutoff)
network.generate_graph(output_dir='reaction_network_output_dim4')
