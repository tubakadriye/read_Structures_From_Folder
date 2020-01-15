'''
Kadriye Tuba Turkcan 08.01.2019
This program reads xyz files inside the Structures folder
appends the names of these files into a list
Gets number of atoms, energy values and cell parameters of each structure
and adds these into corresponding lists
calculates the volume of each cell of each structure
puts name of  the structure, number of atoms, energy values, cell volume into a pandas dataframe
sorts the values in the dataframe according to energy values in ascending order

'''

import sys
import os
from pathlib import Path  #for getting the path of Structures
import glob
import subprocess
from subprocess import PIPE, Popen
import numpy as np
import pandas as pd

'''def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0].decode("UTF-8")'''


#xyz_files=[]

# get xyz files inside Structures folder
xyz_files=[x for x in os.listdir(".\Structures") if x.endswith(".xyz")]

print('xyz files: ', xyz_files)

#lists for nb of atoms, energy values, structure names, cell volumes
nAtom=[]
energy_vals=[]
structure_names=[]
volumes=[]

for file in xyz_files: #loop over each xyz file
    structure_names.append(file.rstrip(".xyz")) # get the name of the structure and add to list

    Structures=Path("./Structures") #Get the path of structures
    file_to_open=Structures/file  #file inside the given path
    open_file=open(file_to_open,"r") #open file to read
    data=open_file.readlines() #read lines of the file and add to data list

    #print(data)
    for i in range(len(data)):  # loop over the lines of each file
        data[i]=data[i].rstrip("\n") #cut out \n from the right
        #data[i] = data[i].rstrip("\t")
    print()
    print(file, ": ")
    print(data)
    cell_params = []  #list for cell parameters
    nAtom.append(int(data[0]))  # add first value in each file to nAtom list
    energy_vals.append(float(data[1].split()[1])) #add 2nd value of the 2nd line in each file to energy_vals
    for i in range(4,len(data[1].split())): #loop over the cell parameters
        cell_params.append(float(data[1].split()[i])) #add cell parameters to list

    print("cell parameters = ", cell_params)
    cell_matrix = []  #matrix of cell parameters
    #for i in range(7):
        #cell_matrix.append(cell_params[i:i+3])
    cell_matrix.append(cell_params[0:3])
    cell_matrix.append(cell_params[3:6])
    cell_matrix.append(cell_params[6:9])
    np_cell_matrix=np.array(cell_matrix)  #convert cell matrix to np array
    print("cell matrix = ",cell_matrix)
    print(np_cell_matrix)
    determinant=np.linalg.det(np_cell_matrix) #determinant of the cell matrix
    print("determinant = %10.5f" %determinant)
    volume=abs(determinant) #cell volume
    volumes.append(volume) #add each volume to volumes array
    print("volume = %10.5f" %volume)



print()
print()
print("structure names = ",len(structure_names),structure_names)
print("nAtom = ",len(nAtom),nAtom)
print("energy values = " ,len(energy_vals),energy_vals)
print("volumes = " ,len(volumes), volumes)

#print(compound_names[0])

#make a list to use for the pandas dataframe
pandas_data=[[0 for x in range(4)] for y in range(9)]


#pandas_data[0][0]=compound_names[0]
#pandas_data[1][0]=compound_names[1]
#pandas_data[2][0]=compound_names[2]
#print (pandas_data[0][0])
for i in range(9): #loop over the structures
    pandas_data[i][0]=structure_names[i] #assign structure names to the first array element of each array of pandas_data
    pandas_data[i][1]=nAtom[i] # assign nAtom to the second array element of each array of pandas_data
    pandas_data[i][2]=energy_vals[i] #assign energy vals to the third array element of each array of pandas_data
    pandas_data[i][3]=volumes[i] ##assign volumes to the fourth array element of each array of pandas_data

print("\npandas data: ", pandas_data)
np_pandas_data=np.array(pandas_data) #to show the pandas_data in a matrix form convert to np-array
print("pandas data: ")
print(np_pandas_data)

#pandas data frame made by pandas_data list
dataframe=pd.DataFrame(pandas_data,columns=['Structure Name', 'Nb of Atoms','Energy','Cell Volume'])

#print(dataframe)
print()
#sort Dataframe by energy values
sort_by_energy=dataframe.sort_values('Energy')
print(sort_by_energy)












'''for file in glob.glob("*.xyz",recursive=True):
    xyz_files.append(file)'''

#xyz_files=cmdline("find ./Structures/ -maxdepth 1 -name '*.xyz'").split()

#xyz_files=cmdline("dir .\Structures\ -name '*.xyz'").split()




