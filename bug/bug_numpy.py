
import logging
from logging import getLogger

import numpy as np
from scipy.spatial import Delaunay,distance
import matplotlib.pyplot as plt

np.random.seed(100)

class SwarmSim():
    def __init__(self,n:int,step:int=5, logger=None) -> None:
        self.n = n
        self.hist_pos = np.zeros((step,n,2))
        self.hist_v = np.zeros((step,n,2))
        
        self.position = np.random.rand(n,2)
        self.hist_pos[0] = self.position

        self.vector = np.random.uniform(-0.1,0.1,(n,2)) 
        self.hist_v[0] = self.vector

        self.th_rep = 0.1
        self.th_attr = 0.15

        self.dist_matrix = self.get_dist_matrix()

        # 遠すぎる
        print(np.where(self.dist_matrix > self.th_attr, 1, 0))
        # 近すぎる
        print(np.where((self.dist_matrix < self.th_rep) & (self.dist_matrix != 0), 1, 0))
        self.draw()

    def move(self):
        pass

    
    def get_dist_matrix(self):
        dist_matrix = distance.cdist(self.position,self.position, metric='euclidean')
        return dist_matrix
    
    def draw(self):
        xy = self.position

        fig,ax = plt.subplots()
        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
        ax.set_aspect("equal")
        ax.scatter(xy[:,0],xy[:,1])
        
        v = self.vector
        ax.quiver(xy[:,0],xy[:,1],v[:,0],v[:,1],angles="xy",scale_units="xy",scale=1)
        
        for i in range(self.n):
            ax.text(xy[i,0],xy[i,1],i)

        # 各中心点に対して円を描く
        radius = self.th_rep
        
        for center in xy:
            theta = np.linspace(0, 2 * np.pi, 100)
            x = center[0] + radius * np.cos(theta)
            y = center[1] + radius * np.sin(theta)
            ax.plot(x,y,c="blue", alpha=0.2)

            x = center[0] + self.th_attr * np.cos(theta)
            y = center[1] + self.th_attr * np.sin(theta)
            ax.plot(x,y,c="red", alpha=0.2)


        plt.show()
