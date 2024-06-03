import os
import bug_numpy

import numpy as np
from scipy.spatial import distance

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# gif 作成
pos_data = np.load("sim_position.npy")
v_data = np.load("sim_vector.npy")

# アニメーションの設定
fig, ax = plt.subplots()
ax.grid()
line, = ax.plot([], [], 'bo', markersize=10)
sc, = ax.plot([],[], "o",color="gray", markersize=10, alpha=0.2)
texts = [ax.text(0, 0, '', ha='center', va='center') for _ in range(20)]  # Text objects for each point
arrs = [ax.arrow(0, 0, 0, 0,shape="full",length_includes_head=True) for _ in range(20)]
# scat = ax.scatter([],[],color="red")
ax.set_xlim(-25, 25)
ax.set_ylim(-25, 25)
ax.set_aspect("equal")
# 初期化関数
def init():
    for text in texts:
        text.set_text('')  # Clears all text

    sc.set_data([], [])
    # line.set_data([], [])
    return sc,

# フレーム更新関数
def update(frame):
    # ax.scatter(data[frame,:,0], data[frame,:,1])
    
    # scat.set_offsets(pos_data[frame])#(pos_data[frame,:,0], pos_data[frame,:,1])
    for i in range(20):
        texts[i].set_position(pos_data[frame,i])  # Resets all text positions
        texts[i].set_text(i)  # Clears all text

        arrs[i].set_data(x=pos_data[frame,i,0],y=pos_data[frame,i,1], dx=v_data[frame,i,0], dy=v_data[frame,i,1],width=0.003)
    # ax.quiver(pos_data[frame,:,0], pos_data[frame,:,1],v_data[frame,:,0],v_data[frame,:,1])
    # print(*pos_data[frame,0])

    sc.set_data(pos_data[frame,:,0], pos_data[frame,:,1])
    return sc,

# アニメーションの作成
ani = animation.FuncAnimation(fig, update, frames=20, init_func=init, blit=True)

# GIFとして保存
ani.save('animation.gif', writer='pillow', fps=2)



exit()
bug_numpy.SwarmSim(20,30)