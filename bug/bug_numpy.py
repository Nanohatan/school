
import logging
import os
from logging import getLogger

import numpy as np
from scipy.spatial import Delaunay,distance
import matplotlib.pyplot as plt

np.random.seed(100)

class SwarmSim():
    def __init__(self,n:int,nstep:int=5, logger=None) -> None:
        self.n = n
        self.hist_pos = np.zeros((nstep,n,2))
        self.hist_v = np.zeros((nstep,n,2))
        
        self.position = np.random.uniform(-5,5,(n,2))
        self.hist_pos[0] = self.position

        self.vector = np.random.uniform(-0.1,0.1,(n,2)) 
        # ベクトルのノルムを計算
        norms = np.linalg.norm(self.vector, axis=1)
        # 各ベクトルをそのノルムで割って単位ベクトルを計算
        self.vector  = self.vector / norms[:, np.newaxis]
        self.hist_v[0] = self.vector 

        self.intract_r = 2
        self.th_rep = 1
        self.th_attr = 1.5
        
        self.draw()
        for step in range(nstep):
            self.next_step()
            self.draw(f"{step}_")
            

    def next_step(self):
        dist_matrix = self.get_dist_matrix()
        intract_matrix = np.where((dist_matrix < self.intract_r), 1, 0)
        self.update_v(intract_matrix)

        self.update_pos()

    def update_v(self,m):
        vector = np.zeros((self.n,2))
        for i in range(m.shape[0]):
            #自身を含めて隣接する個体の速度の平均を計算
            v = np.divide(np.dot(self.vector.T,m[i]), np.sum(m[i]))
            vector[i] = v
        
        self.vector = self.to_unit(vector)


    def update_pos(self):
        self.position = self.position + self.vector

    
    def get_dist_matrix(self):
        dist_matrix = distance.cdist(self.position,self.position, metric='euclidean')
        return dist_matrix
    
    def to_unit(self,v):
        norms = np.linalg.norm(v, axis=1)
        # 各ベクトルをそのノルムで割って単位ベクトルを計算
        return v / norms[:, np.newaxis]

    def draw(self,fn="init"):
        xy = self.position

        fig,ax = plt.subplots()
        lim = 10
        ax.set_xlim(-lim,lim)
        ax.set_ylim(-lim,lim)
        ax.set_aspect("equal")
        ax.grid()
        ax.scatter(xy[:,0],xy[:,1])
        
        v = self.vector
        ax.quiver(xy[:,0],xy[:,1],v[:,0],v[:,1],angles="xy",scale_units="xy",scale=1)
        
        for i in range(self.n):
            ax.text(xy[i,0],xy[i,1],i)

        # 各中心点に対して円を描く
        radius = self.intract_r
        
        for center in xy:
            theta = np.linspace(0, 2 * np.pi, 100)
            x = center[0] + radius * np.cos(theta)
            y = center[1] + radius * np.sin(theta)
            ax.plot(x,y,c="blue", alpha=0.2)

            # x = center[0] + self.th_attr * np.cos(theta)
            # y = center[1] + self.th_attr * np.sin(theta)
            # ax.plot(x,y,c="red", alpha=0.2)

        plt.tight_layout()
        dir = os.path.dirname(__file__)

        fig.savefig(os.path.join(dir,"img",fn))
        plt.close()
