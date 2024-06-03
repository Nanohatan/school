
import logging
import os
from logging import getLogger

import numpy as np
from scipy.spatial import Delaunay,distance
import matplotlib.pyplot as plt
import imageio
import glob
np.random.seed(100)

class SwarmSim():
    def __init__(self,n:int,nstep:int=20, logger=None) -> None:
        self.n = n
        self.hist_pos = np.zeros((nstep,n,2))
        self.hist_v = np.zeros((nstep,n,2))
        
        field = 10
        self.position = np.random.uniform(-field,field,(n,2))
        self.hist_pos[0] = self.position

        self.vector = np.random.uniform(-0.1,0.1,(n,2)) 
        # ベクトルのノルムを計算
        norms = np.linalg.norm(self.vector, axis=1)
        # 各ベクトルをそのノルムで割って単位ベクトルを計算
        self.vector  = self.vector / norms[:, np.newaxis]
        self.hist_v[0] = self.vector 

        self.intract_r = 4
        self.th_rep = 1
        self.th_attr = 1.5
        self.speed = 1


        # シミュレーション実行
        for step in range(nstep):
            #self.draw(f"{str(step).zfill(3)}_")
            self.next_step(step)
        #self.draw(f"{str(step).zfill(3)}_")
        np.save("sim_position",self.hist_pos)
        np.save("sim_vector",self.hist_v)
        # gif 作成
        matrix = np.load("sim_position.npy")
        
        print(matrix.shape)

        # dir = os.path.dirname(__file__)
        # list_of_im_paths = sorted(glob.glob(os.path.join(dir,"img/**.png")))
        # path_to_save_gif = os.path.join(dir,"img/ani.gif")
        # ims = [imageio.imread(f) for f in list_of_im_paths]
        # imageio.mimwrite(path_to_save_gif, ims,loop=0)
            


    
    def next_step(self,step):
        dist_matrix = self.get_dist_matrix()
        intract_matrix = np.where((dist_matrix < self.intract_r), 1, 0)

        self.update_v(intract_matrix)
        self.update_pos()

        self.hist_v[step] = self.vector
        self.hist_pos[step] = self.position

    def update_v(self,m):
        vector = np.zeros((self.n,2))
        for i in range(m.shape[0]):
            #自身を含めて隣接する個体の速度の平均を計算
            v = np.divide(np.dot(self.vector.T,m[i]), np.sum(m[i]))
            vector[i] = v
        
        self.vector = self.to_unit(vector) + np.random.uniform(-0.5,0.5,(self.n,2))


    def update_pos(self):
        self.position = self.position + self.speed*self.vector

    
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
        lim = 25
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
            ax.plot(x,y,c="blue", alpha=0.1)

            # x = center[0] + self.th_attr * np.cos(theta)
            # y = center[1] + self.th_attr * np.sin(theta)
            # ax.plot(x,y,c="red", alpha=0.2)

        plt.tight_layout()
        dir = os.path.dirname(__file__)

        fig.savefig(os.path.join(dir,"img",fn))
        plt.close()
