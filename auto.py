import numpy as np
import matplotlib.pyplot as plt
np.random.seed(10)
# 環境の初期化
environment_size = (100, 100)
num_animals = 10
positions = np.random.rand(num_animals, 2) * environment_size
velocity = np.ones((num_animals, 2)) * 5  # 各動物の速度を一定とする
attraction_constants = (1, -1, 1, -1)  # 引力/斥力の定数(a, b, c, d)
momentum_percent = 0.5
attraction_percent = 0.5
steps_between_random_movement = 15

def calculate_distance(pos1, pos2):
    return np.linalg.norm(pos1 - pos2)

def attraction_repulsion_force(distance, a, b, c, d):
    return (distance**a - b) / (distance**c + d)

def normalize_vector(vec):
    norm = np.linalg.norm(vec)
    if norm == 0: 
        return vec
    return vec / norm

# シミュレーションの実行
num_steps = 30
result = np.zeros((num_steps,num_animals,2))
for step in range(num_steps):
    result[step] = positions
    for i in range(num_animals):
        movement_vector = np.zeros(2)
        for j in range(num_animals):
            if i != j:
                distance = calculate_distance(positions[i], positions[j])
                force = attraction_repulsion_force(distance, *attraction_constants)
                direction = normalize_vector(positions[j] - positions[i])
                movement_vector += direction * force
        
        # 運動量と引力/斥力の組み合わせ
        momentum_vector = normalize_vector(velocity[i]) * momentum_percent
        attraction_vector = normalize_vector(movement_vector) * attraction_percent
        combined_vector = momentum_vector + attraction_vector
        
        # 速度の正規化と更新
        velocity[i] = normalize_vector(combined_vector) * np.linalg.norm(velocity[i])
        
        # ランダムな動き
        if step % steps_between_random_movement == 0:
            random_direction = np.random.rand(2) - 0.5
            velocity[i] += normalize_vector(random_direction) * np.linalg.norm(velocity[i]) * 0.1
            
        positions[i] += velocity[i]
        
        # 環境内での位置の制限 (オプション)
        positions[i] = np.clip(positions[i], 0, environment_size[0])

    # シミュレーションの状態を描画するコードをここに追加（例: matplotlibを使用）

fig,ax = plt.subplots()
for i in range(num_animals):
    ax.plot(result[:,i,0],result[:,i,1])
plt.show()
