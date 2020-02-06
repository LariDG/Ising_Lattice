"""
Modelling and Visualisation in Physics
Checkpoint 1: Ising Lattice
Main for Ising Lattice
Author: L. Dorman-Gajic
"""
from Ising_Lattice import Ising_Lattice
import numpy as np 
import random
import sys


def main():
    
    if len(sys.argv) != 2:         
        print("input:" + sys.argv[0] + "animation or <parameters file>" + "<Glauber or Kawasaki file>")
        quit()
    
    if sys.argv[1] == "animation":      
        temp = float(input("temperature?"))
        size_input = int(input("size of lattice?"))
        dynamics = str(input("Glauber or Kawasaki?"))
        spin = str(input("random, up, or down?"))
        size = (size_input, size_input)

        lattice = Ising_Lattice(temp, size, dynamics, spin)
        lattice.run(10000, 1000)
    
    else:  
            
        input_file = sys.argv[1]
        infile = open(input_file, "r")
        parameters = infile.readline()
        parameters_list = parameters.split()
        min_temp = float(parameters_list[0])
        max_temp = float(parameters_list[1])
        size = (int(parameters_list[2]), int(parameters_list[2]))
        dynamics = str(parameters_list[3])
        spin = str(parameters_list[4])

        sweeps = 10000 #number of sweeps for each temperature
        equil_s = 100 #number of sweeps until system equilibrates
        collect = 10 #number of sweeps between each measurement

        energy = [] #opening a list for energy
        magnetisation = [] #opening a list for magnetisation
        heat_c = [] #opening a list for heat capacity 
        suseptibility = [] #opening a list for suseptibility
        temp_list = []
        heat_c_error = []
        sus_error = []

        temp_range = np.arange(min_temp, max_temp, 0.1) #creating an array of temperatures between min and max temperature with 30 evenly spaced points     
        print(size)
        print(size)
        print(min_temp)
        print(max_temp)
        print(dynamics)
        
        for t in range(len(temp_range)):
           
            lattice = Ising_Lattice(temp = temp_range[t], size = size, dynamics = dynamics, spin = spin)
            E_single_temp = []
            M_single_temp = []            

            if lattice.dynamics == "Glauber":
                for i in range(sweeps):                                    
                    for j in range(size[0]*size[1]):
                        lattice.Glauber()
                        if i % collect == 0 and i >= equil_s:                           
                            E_single_temp.append(lattice.energy_total())
                            M_single_temp.append(lattice.magnetisation())

            energy.append(lattice.average(E_single_temp))
            magnetisation.append(lattice.average(M_single_temp))
            heat_c.append(lattice.heat_cap(E_single_temp))
            heat_c_error.append(lattice.errors_heat_cap(E_single_temp))
            suseptibility.append(lattice.suseptibility(M_single_temp))
            sus_error.append(lattice.errors_sus(M_single_temp))

            file_handle = open("Glauber.dat", "w+")
            file_handle.write('%lf, %lf, %lf, %lf, %lf, %lf, %lf\n' % (temp_range[t], energy[t], heat_c[t], heat_c_error[t], magnetisation[t], suseptibility[t], sus_error[t]))
                

            if lattice.dynamics == "Kawasaki":  
                for i in range(sweeps):                  
                    for j in range(size**2):
                        lattice.Kawasaki()
                        if i % collect == 0 and i >= equil_s:
                            E_single_temp.append(lattice.energy_total)
                            M_single_temp.append(lattice.magnetisation)

            energy.append(lattice.average(E_single_temp))
            heat_c.append(lattice.heat_cap(E_single_temp))
            heat_c_error.append(lattice.errors_heat_cap(E_single_temp))
            
            file_handle = open("Kawasaki.dat", "w")
            file_handle.write('%lf, %lf, %lf, %lf\n' % (temp_range[t], energy[t], heat_c[t], heat_c_error[t]))
        
        file_handle.close()
        input_file.close()
       
main()
