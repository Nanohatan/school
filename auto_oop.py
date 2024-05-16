import numpy as np
import matplotlib.pyplot as plt
np.random.seed(10)

class Animal:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def update_position(self, movement):
        self.position += movement
        self.position = np.clip(self.position, 0, 100)  # 環境サイズに依存するため、100に設定

class Simulation:
    def __init__(self, num_animals, environment_size):
        self.num_animals = num_animals
        self.environment_size = environment_size
        self.positions = np.random.rand(num_animals, 2) * environment_size
        self.velocity = np.ones((num_animals, 2)) * 5
        self.animals = [Animal(pos, vel) for pos, vel in zip(self.positions, self.velocity)]
        self.attraction_constants = (1, -1, 1, -1)  # 引力/斥力の定数(a, b, c, d)
        self.momentum_percent = 0.5
        self.attraction_percent = 0.5

    def calculate_distance(self, pos1, pos2):
        return np.linalg.norm(pos1 - pos2)

    def attraction_repulsion_force(self, distance):
        a, b, c, d = self.attraction_constants
        return (distance**a - b) / (distance**c + d)

    def normalize_vector(self, vec):
        norm = np.linalg.norm(vec)
        if norm == 0:
            return vec
        return vec / norm

    def run_simulation(self, num_steps):
        result = np.zeros((num_steps, self.num_animals, 2))
        for step in range(num_steps):
            for i, animal_i in enumerate(self.animals):
                movement_vector = np.zeros(2)
                for j, animal_j in enumerate(self.animals):
                    if i != j:
                        distance = self.calculate_distance(animal_i.position, animal_j.position)
                        force = self.attraction_repulsion_force(distance)
                        direction = self.normalize_vector(animal_j.position - animal_i.position)
                        movement_vector += direction * force
                
                momentum_vector = self.normalize_vector(animal_i.velocity) * self.momentum_percent
                attraction_vector = self.normalize_vector(movement_vector) * self.attraction_percent
                combined_vector = momentum_vector + attraction_vector
                animal_i.velocity = self.normalize_vector(combined_vector) * np.linalg.norm(animal_i.velocity)
                animal_i.update_position(animal_i.velocity)
                
                result[step, i] = animal_i.position
                
        return result

# シミュレーションの実行
simulation = Simulation(num_animals=10, environment_size=(100, 100))
result = simulation.run_simulation(30)

# 結果の描画
fig, ax = plt.subplots()
for i in range(10):
    ax.plot(result[:, i, 0], result[:, i, 1])

fig.savefig("oop.png")
