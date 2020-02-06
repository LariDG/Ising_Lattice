import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from Ising_Lattice import Ising_Lattice
import time

dynamics = input("Glauber or Kawasaki?")
spin = input("random, up, or down?")

lattice = Ising_Lattice(5, (50,50), dynamics, spin)
lattice.run(10000, 1000)

