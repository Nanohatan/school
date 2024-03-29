import numpy as np
np.random.seed(100)
class school():
    def __init__(self) -> None:
        self.fish_list = []
        # for id in range(n):
        #     v = np.random.rand(2)
        #     self.fish_list.append(fish(id,v=np.random.rand(2),position=((np.random.rand(2))*10)+[50,50]))
            
        # self.fish_list = np.array(self.fish_list)
    def create_fish(self,params,n):
        for _ in range(n):
            id = len(self.fish_list)
            _fish = fish(id,v=np.random.rand(2),position=((np.random.rand(2))*10)+[50,50],
                         params=params["params"])
            self.fish_list.append(_fish)
        
    def simulate(self,n_step):
        for step in range(n_step):
            if step%15 == 0:
                pass
            else:
                self.update()
    def update(self):
        for ind in range(len(self.fish_list)):
            self.fish_list[ind].update(np.delete(self.fish_list, ind))
        for i in self.fish_list:
            i.position = i.history[-1]
            i.v = i.v_history[-1]
    def random_move(self):
        # todo add random move to fish
        for ind in range(len(self.fish_list)):
            self.fish_list[ind].update(np.delete(self.fish_list, ind))
        for i in self.fish_list:
            i.position = i.history[-1]
            i.v = i.v_history[-1]
    def get_position(self):
        xy = []
        for fish in self.fish_list:
            xy.append(fish.history[-1])
        xy = np.array(xy)
        return xy
    def get_history(self):
        matrix = []
        for fish in self.fish_list:
            matrix.append(fish.history)
        return np.array(matrix)
    

class fish():
    def __init__(self, id, v, position, params):
        self.id = id
        self.v = params["velocity"] * v/np.linalg.norm(v)
        self.position = position
        self.history = [position]
        self.v_history = [self.v]
        
        #params
        self.a=params["a"]
        self.b=params["b"]
        self.c=params["c"]
        self.d=params["d"]
        self.alpha = params["moumentum"]

    def update(self,neighbors):
        total_f = self.get_total_f(neighbors)
        print(total_f)
        next_v = (total_f + self.alpha*self.v)/np.linalg.norm((total_f + self.alpha*self.v))

        next_position = self.position + self.v
        self.history.append(next_position)
        self.v_history.append(next_v)
    def get_total_f(self,neighbors):
        total_f = 0
        for j in neighbors:
            total_f += self.get_f(j)
        return total_f
    
    
    def get_f(self,j):
        e_ij = self.get_e(j)
        r_ij = self.get_r(j)#i-j distance
        f_ij = ((r_ij**self.a)-self.b)/((r_ij**self.c)+self.d)*e_ij
        return f_ij
    
    def get_r(self,j):
        r_ij = np.linalg.norm(self.position-j.position)
        return r_ij
        
    def get_e(self,j):
        r_ij = self.get_r(j)
        e_ij = (self.position-j.position)/r_ij
        return e_ij
    