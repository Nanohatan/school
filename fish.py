import numpy as np
np.random.seed(100)
class school():
    """
    Represents a school of fish with simulation capabilities.

    Attributes:
        fish_list (list of _fish): List of fish in the school.
        fish_type_list (list of str): List of fish type names in the school.
    """
    def __init__(self) -> None:
        """
        Initializes a school object with empty fish lists.
        """

        self.fish_list = []
        self.fish_type_list = []
        # for id in range(n):
        #     v = np.random.rand(2)
        #     self.fish_list.append(fish(id,v=np.random.rand(2),position=((np.random.rand(2))*10)+[50,50]))
            
        # self.fish_list = np.array(self.fish_list)
    def create_fish(self,json,n):
        """
        Creates and adds fish to the school.

        Args:
            json (dict): JSON object containing fish type name and parameters.
            n (int): Number of fish to create.
        """


        self.fish_type_list.append(json["name"])
        for _ in range(n):
            id = len(self.fish_list)
            _f = _fish(id,v=np.random.rand(2),position=((np.random.rand(2))*10)+[50,50],
                         json=json)
            self.fish_list.append(_f)

    def simulate(self,n_step):
        """
        Simulates the movement of fish in the school for a given number of steps.

        Args:
            n_step (int): Number of simulation steps.
        """

        for step in range(n_step):
            if step%15 == 0:
                pass
            else:
                self.update()
    def update(self):
        """
        Updates the positions and velocities of all fish in the school.
        """

        for ind in range(len(self.fish_list)):
            self.fish_list[ind].move(np.delete(self.fish_list, ind))
        for i in self.fish_list:
            i.position = i.history[-1]
            i.v = i.v_history[-1]
    def random_move(self):
        """
        Applies a random movement update to all fish in the school.
        """

        # todo add random move to fish
        for ind in range(len(self.fish_list)):
            self.fish_list[ind].update(np.delete(self.fish_list, ind))
        for i in self.fish_list:
            i.position = i.history[-1]
            i.v = i.v_history[-1]
    def get_position(self):
        """
        Gets the current positions of all fish in the school grouped by type.

        Returns:
            dict: A dictionary with fish type names as keys and arrays of positions as values.
        """

        xy = {}
        for name in self.fish_type_list:
            xy[name] = []
        for fish in self.fish_list:
            xy[fish.type_name].append(fish.history[-1])
        #xy = np.array(xy)
        for name in self.fish_type_list:
            xy[name] = np.array(xy[name])
        return xy
    def get_history(self):
        """
        Gets the movement history of all fish in the school.

        Returns:
            numpy.ndarray: A matrix where each row corresponds to a fish's position history.
        """

        matrix = []
        for fish in self.fish_list:
            matrix.append(fish.history)
        return np.array(matrix)
    

class  _fish():
    """
    Represents a fish with movement behavior influenced by its neighbors.

    Attributes:
        id (int): Unique identifier for the fish.
        type_name (str): The type name of the fish.
        v (numpy.ndarray): The velocity of the fish.
        position (numpy.ndarray): The current position of the fish.
        history (list): A list of positions representing the fish's movement history.
        v_history (list): A list of velocities representing the fish's velocity history.
        a (float): Parameter a for force calculation.
        b (float): Parameter b for force calculation.
        c (float): Parameter c for force calculation.
        d (float): Parameter d for force calculation.
        alpha (float): Momentum factor for velocity update.
    """
    def __init__(self, id, v, position, json):
        """
        Initializes a _fish object.

        Args:
            id (int): Unique identifier for the fish.
            v (numpy.ndarray): Initial velocity vector of the fish.
            position (numpy.ndarray): Initial position vector of the fish.
            json (dict): JSON object containing fish type name and movement parameters.
        """        
        self.id = id
        self.type_name = json["name"]
        params = json["params"]
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

    def move(self,neighbors):
        """
        Updates the fish's position and velocity based on its neighbors.

        Args:
            neighbors (list of _fish): List of neighboring fish.
        """
        total_f = self.get_total_f(neighbors)
        next_v = (total_f + self.alpha*self.v)/np.linalg.norm((total_f + self.alpha*self.v))

        next_position = self.position + self.v
        self.history.append(next_position)
        self.v_history.append(next_v)

    def get_total_f(self,neighbors):
        """
        Calculates the total force acting on the fish from its neighbors.

        Args:
            neighbors (list of _fish): List of neighboring fish.

        Returns:
            numpy.ndarray: The total force vector.
        """        
        total_f = 0
        for j in neighbors:
            total_f += self.get_f(j)
        return total_f
    
    
    def get_f(self,j):
        """
        Calculates the force exerted by a neighboring fish.

        Args:
            j (_fish): A neighboring fish.

        Returns:
            numpy.ndarray: The force vector exerted by the neighbor.
        """        
        e_ij = self.get_e(j)
        r_ij = self.get_r(j)#i-j distance
        f_ij = ((r_ij**self.a)-self.b)/((r_ij**self.c)+self.d)*e_ij
        return f_ij
    
    def get_r(self,j):
        """
        Calculates the distance to a neighboring fish.

        Args:
            j (_fish): A neighboring fish.

        Returns:
            float: The distance between this fish and the neighbor.
        """        
        r_ij = np.linalg.norm(self.position-j.position)
        return r_ij
        
    def get_e(self,j):
        """
        Calculates the unit vector pointing from this fish to a neighboring fish.

        Args:
            j (_fish): A neighboring fish.

        Returns:
            numpy.ndarray: The unit vector pointing towards the neighbor.
        """        
        r_ij = self.get_r(j)
        e_ij = (self.position-j.position)/r_ij
        return e_ij
    