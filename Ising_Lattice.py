"""
Modelling and Visualisation in Physics
Checkpoint 1: Isling Lattice
Class to produce a 2 dimensional lattice of spin up and down components
via the Isling Model.
Author: L. Dorman-Gajic
"""

import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import math


class Ising_Lattice(object):
    def __init__(self, temp, size, dynamics, spin):
        """
            initialising Isling Lattice

            :param temp: temperature as a float
            :param size: size of 2d lattice as a tuple
            :param dynamics: the dynamics of the flipping
            :param spin: the initial spin of lattice           
        """
        self.size = size
        self.temp = temp
        self.dynamics = dynamics
        self.spin = spin
        self.build()

    def build(self):
        """
        Building the lattice from inputted spin preference of random, all up 
        or all down. A 2d matrix is formed of up spins equalling 1 and down spins
        equalling -1.
        """

        if self.spin == "random":
            self.lattice = np.random.choice(a=[1,-1], size=self.size)

        if self.spin == "up":
            self.lattice = np.ones(self.size, dtype=int)

        if self.spin == "half":
            up = np.ones((50,25), dtype=int)
            down = -np.ones((50,25), dtype=int)
            self.lattice = np.append(up, down, axis=1)
            print(self.lattice.shape)

    def pbc(self, indices):
        """
        Applies periodic boundary conditions to correct particles' nearest neighbours

        :param indicies: position in lattice as a tuble
        """
        return(indices[0]%self.size[0], indices[1]%self.size[1])

    def average(self, l):
        array = np.array(l)
        return np.mean(array)
    
    def squared_average(self, l):
        array = np.array(l)
        return np.mean(array**2)

    def energy_change(self, indices):
        """
        Calculating the change of energy if a point on the lattice were to be flipped

        :param indicies: position in lattice as a tuble
        """
        n, m = indices
        energy_change = 2 * self.lattice[n,m] * (self.lattice[self.pbc((n,m-1))] + self.lattice[self.pbc((n,m+1))] + self.lattice[self.pbc((n-1,m))] + self.lattice[self.pbc((n+1,m))])        
        return(energy_change)

    def energy_total(self):
        """
        Calculating the energy for the entire lattice 
        """
        energy_total = 0.0
        for n in range(self.size[0]):
            for m in range (self.size[1]):
                energy_total += -self.lattice[n,m] * (self.lattice[self.pbc((n,m-1))] + self.lattice[self.pbc((n,m+1))] + self.lattice[self.pbc((n-1,m))] + self.lattice[self.pbc((n+1,m))])
        return(energy_total/2)

    def magnetisation(self):
        """
        Calculation of the magnetisation of the lattice.
        The sum of the spin at each lattice point.
        """
        magnetisation = abs(np.sum(self.lattice))
        return(magnetisation)

    def Glauber(self):
        """
        A method in which to flip lattice points in accordance with Glauber dynamics
        The conditions of flipping being if energy change is less than or equal to 1
        or based on the probability function, using random.
        """
        indices = (np.random.randint(0, self.size[0]), np.random.randint(0, self.size[1]))
            
        if self.energy_change(indices) <= 0.0:
            self.lattice[indices] *= -1
        elif np.random.rand() <= np.exp(-self.energy_change(indices)/self.temp):        
            self.lattice[indices] *= -1

    def Kawasaki(self):
        """
        A method in which to flip lattice points in accordance with Kawasaki dynamics 
        where two points swap if they are of opposite spin. 
        Same as with Glauber but now taking two spins into account
        """
        indices_a = (np.random.randint(0, self.size[0]), np.random.randint(0, self.size[1]))
        indices_b = (np.random.randint(0, self.size[0]), np.random.randint(0, self.size[1]))

        if self.lattice[indices_a] == -self.lattice[indices_b]:
               
            change_e_a = self.energy_change(indices_a)               
            self.lattice[indices_a] *= -1
            change_e_b = self.energy_change(indices_b)
            self.lattice[indices_a] *= -1

            if (change_e_a + change_e_b) <= 0.0:
                self.lattice[indices_a] *= -1
                self.lattice[indices_b] *= -1

            elif np.random.rand() <= np.exp(-(change_e_a + change_e_b)/self.temp):
                self.lattice[indices_a] *= -1
                self.lattice[indices_b] *= -1

    def heat_cap(self, energy_list):
        heat_cap = (1/((self.size[0]*self.size[1])*(self.temp**2))*(np.var(energy_list)))
        return(heat_cap)

    def errors_heat_cap(self, energy):
        errors = []
        for i in range(100):
            data_point = []
            for j in range(len(energy)):
                data_point.append(energy[np.random.choice(len(energy))])
            errors.append(self.heat_cap(data_point))
        return math.sqrt(np.var(errors))

    def susceptibility(self, mag_list):        
        susceptibility = (1/((self.size[0]*self.size[1])*self.temp)*(np.var(mag_list)))
        return(susceptibility)

    def errors_sus(self, mag):
        errors = []
        for i in range(100):
            data_point = []
            for j in range(len(mag)):
                data_point.append(mag[np.random.choice(len(mag))])
            errors.append(self.susceptibility(data_point))
        return math.sqrt(np.var(errors))

    def run(self, iterations, it_per_frame):
        """
        method running the data into FuncAnimation
        """
        self.it_per_frame = it_per_frame
        self.figure = plt.figure()
        self.image = plt.imshow(self.lattice, animated=True)
        self.animation = animation.FuncAnimation(self.figure, self.animate, repeat=False, frames=iterations, interval=100, blit=True)
        plt.show()

    def animate(self, *args):
        """
        a loop to but data into animation
        """
        for i in range(self.it_per_frame):
            if self.dynamics == "Glauber":
                self.Glauber()
            elif self.dynamics == "Kawasaki":
                self.Kawasaki()
        self.image.set_array(self.lattice)
        return self.image,
