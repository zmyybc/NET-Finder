import numpy as np
from ase import Atoms
from ase.io import write
from ase.calculators.emt import EMT
from net_finder.paths import TransitionStateSearch
from net_finder.net import ReactionNetwork

def create_cu_cluster(positions):
    cluster = Atoms('Cu4', positions=positions)
    cluster.set_pbc(False)  # 明确设置为非周期性
    cluster.center(vacuum=5.0)  # 在周围添加真空，并将团簇居中
    return cluster

# 创建初始结构（4个铜原子的不同排列）
structures = [
    create_cu_cluster([
        (0, 0, 0),
        (2.5, 0, 0),
        (1.25, 2.165, 0),
        (1.25, 0.722, 2.165)
    ]),  # 四面体构型
    create_cu_cluster([
        (0, 0, 0),
        (2.5, 0, 0),
        (1.25, 2.165, 0),
        (3.75, 2.165, 0)
    ]),  # 平面菱形构型
    create_cu_cluster([
        (0, 0, 0),
        (2.5, 0, 0),
        (5.0, 0, 0),
        (7.5, 0, 0)
    ]),  # 直线构型
    create_cu_cluster([
        (0, 0, 0),
        (2.5, 0, 0),
        (0, 2.5, 0),
        (2.5, 2.5, 0)
    ])  # 平面正方形构型
]

# 稍微扰动每个结构以增加多样性
for structure in structures:
    structure.positions += np.random.rand(*structure.positions.shape) * 0.1
    structure.center(vacuum=5.0)  # 重新居中并确保有足够的真空

# 保存初始结构
for i, structure in enumerate(structures):
    write(f'initial/cu_cluster_{i}.xyz', structure)

print(f"创建并保存了 {len(structures)} 个初始结构，每个结构有 {len(structures[0])} 个铜原子。")

# 设置EMT计算器
calc = {
    "calculator_imports": "from ase.calculators.emt import EMT",
    "calculator_setup": "calc = EMT()"
}

# 设置Dimer参数
dimer_params = {
    'displacement_method': 'gauss',
    'displacement_radius': 0.5,
    'dimer_separation': 0.01
}

# 设置运行参数
run_params = {
    'run_mode': 'shell'
}

# 创建TransitionStateSearch对象并运行
ts_search = TransitionStateSearch(structures, calc, dimer_params, output_dir='output', **run_params)
ts_search.run(fmax=0.05, steps=100)

# 收集反应路径
reaction_paths = ts_search.collect_reaction_paths()
print(f"收集到 {len(reaction_paths)} 条反应路径")

# 创建ReactionNetwork对象并生成图形
energy_cutoff =10.0  # 设置一个合适的能量阈值（单位：eV）
network = ReactionNetwork(reaction_paths, energy_cutoff)
network.generate_graph(output_dir='reaction_network_output')

print("反应网络分析完成，结果保存在 'reaction_network_output' 目录中")
