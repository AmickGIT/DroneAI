from matplotlib import pyplot as plt
import numpy as np


class VectorVisualisation:
    def __init__(self):
        # Set up the figure and axis
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim([-1, 1])
        self.ax.set_ylim([-1, 1])
        self.ax.set_zlim([-1, 1])
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")
        self.ax.set_zlabel("Z-axis")

        # Initialize the vector
        self.end_init = np.array([0, 0, 0])  # Example: fixed initial end point
        self.quiver = self.ax.quiver(0, 0, 0, self.end_init[0], self.end_init[1], self.end_init[2], color="r")
        plt.ion() 

    def set_direction(self, direction):
        """
        Update the direction of the vector dynamically.
        :param direction: A 3D vector representing the new direction.
        """
        self.quiver.remove()
        self.quiver = self.ax.quiver(0, 0, 0, direction[0], direction[1], direction[2], color="r")

    def animate(self):
        """
        Show the visualization.
        """
        plt.pause(0.01) 
