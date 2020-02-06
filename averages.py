import numpy as n


def average(l):
    return squared_average = sum(l)/len(l)

def squared_average(l):
    return squared_average = sum(i*i for i in l)/len(l)

def heat_cap(energy_list, temp, size):
    return heat_cap = (1/((size**2)*(temp**2)))*((squared_average(energy_list))-(average(energy_list))**2)

def susceptibility(mag_list, temp, size):
    return susceptibility = (1/((size**2)*temp))*((squared_average(mag_list))-(average(mag_list))**2)
