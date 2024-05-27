
import logging
from logging import getLogger

import numpy as np
from scipy.spatial import Delaunay,distance
import matplotlib.pyplot as plt

np.random.seed(100)



class SwarmSimulation():
    def __init__(self,n,iteration:int) -> None:
        logger = getLogger(__name__)
        logging.basicConfig(filename='SwarmSimulation.log', encoding='utf-8',level=logging.INFO)

        swarm = Swarm(n,logger=logger)
        swarm.draw()
        for step in range(iteration):
            logger.info(f"Step {step}/{iteration}")


class Swarm():
    def __init__(self,n:int, logger=None) -> None:
        self.n = n
        self.swarm = []
        self.swarm_xy = np.zeros((n,2))
        self.swarm_matrix = np.zeros((n,n))

        self.create_bug()

    def move(self):
        pass

    def create_bug(self):
        for i in range(self.n):
            self.swarm.append(Bug()) 


    def get_xy(self):
        for i in range(self.n):
            self.swarm_xy[i] = self.swarm[i].xy

        return self.swarm_xy
    
    def draw(self):
        xy = self.get_xy()
        dist_matrix = distance.cdist(xy,xy, metric='euclidean')

        fig,ax = plt.subplots()
        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
        ax.set_aspect("equal")
        ax.scatter(xy[:,0],xy[:,1])
        for i in range(self.n):
            ax.text(xy[i,0],xy[i,1],i)
        plt.show()

class Bug():
    def __init__(self) -> None:
        self.xy = np.random.rand(2)

    def move(self):
        pass