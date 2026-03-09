import numpy as np
import matplotlib.pyplot as plt
import random

# Maze layout
maze = np.array([
    [1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1],
    [1,0,1,1,1,0,1],
    [1,0,0,0,1,0,1],
    [1,1,1,0,1,0,1],
    [1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1],
])

start = (1,1)
goal = (5,5)

POP_SIZE = 100
DNA_LENGTH = 40
GENERATIONS = 200
MUTATION_RATE = 0.05

moves = [
    (-1,0),  # up
    (1,0),   # down
    (0,-1),  # left
    (0,1)    # right
]

class Agent:
    def __init__(self):
        self.dna = [random.randint(0,3) for _ in range(DNA_LENGTH)]
        self.fitness = 0

    def run(self):
        x,y = start
        hit_wall = False

        for gene in self.dna:
            dx,dy = moves[gene]
            nx,ny = x+dx, y+dy

            if maze[nx,ny] == 1:
                hit_wall = True
                break
            else:
                x,y = nx,ny

            if (x,y) == goal:
                break

        dist = abs(goal[0]-x) + abs(goal[1]-y)

        self.fitness = 1/(dist+1)

        if hit_wall:
            self.fitness *= 0.5

        if (x,y) == goal:
            self.fitness += 1


def crossover(parent1, parent2):
    child = Agent()
    split = random.randint(0, DNA_LENGTH-1)

    child.dna = parent1.dna[:split] + parent2.dna[split:]

    for i in range(DNA_LENGTH):
        if random.random() < MUTATION_RATE:
            child.dna[i] = random.randint(0,3)

    return child


def draw_best(agent, generation):
    x,y = start
    path = [(x,y)]

    for gene in agent.dna:
        dx,dy = moves[gene]
        nx,ny = x+dx,y+dy

        if maze[nx,ny] == 1:
            break

        x,y = nx,ny
        path.append((x,y))

        if (x,y) == goal:
            break

    plt.clf()
    plt.imshow(maze, cmap="gray_r")

    px = [p[1] for p in path]
    py = [p[0] for p in path]

    plt.plot(px, py)
    plt.scatter(start[1],start[0])
    plt.scatter(goal[1],goal[0])

    plt.title(f"Generation {generation}")
    plt.pause(0.5)


population = [Agent() for _ in range(POP_SIZE)]

plt.figure()

for generation in range(GENERATIONS):

    for agent in population:
        agent.run()

    population.sort(key=lambda a: a.fitness, reverse=True)

    best = population[0]

    draw_best(best, generation)

    new_population = population[:10]

    while len(new_population) < POP_SIZE:
        p1 = random.choice(population[:50])
        p2 = random.choice(population[:50])
        child = crossover(p1,p2)
        new_population.append(child)

    population = new_population

plt.show()