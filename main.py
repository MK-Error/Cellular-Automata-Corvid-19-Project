from Cell import Cell
from CellularAutomaton import CellularAutomaton
import matplotlib.pyplot as plt
import imageio
import os

"""
creating list of susceptible,exposed,infected,removed 
creating list of time for ploting
append starting values into lists 
for example:
990 susceptible
10 infected
0 value into others
filenames list for gif generation
"""
susceptible= []
exposed= []
infected= []
removed= []
time = []
susceptible.append(1960/2000)
exposed.append(30/2000)
infected.append(10/2000)
removed.append(0)
time.append(0)
filenames = []

"""
instantiating CellularAutomaton with SEIR values
sorting list of cells by position x and y 
plots initial state of environment
t0 -> does ca.next steps without moving or changing state
plots t0 state

CellularAutomaton(susceptible, exposed, infected, removed, infection_rate, incubation_period, latent_time, spreadrange, ismoving, movedistance)
"""
ca = CellularAutomaton(1960, 30, 10, 0, 0.25, 5, 2, 5, 0.5, 10)
ca.cells.sort(key=lambda cell: (cell.positionX, cell.positionY))

plt.subplot(2,1,1) # creates subplot
for i in ca.cells:
    if i.state == 2: #infected
        plt.plot(i.positionX, i.positionY, 'ro', markersize=2)
    elif i.state == 3: #removed
        plt.plot(i.positionX, i.positionY, 'ko', markersize=2)
    elif i.state == 0: #susceptible
        plt.plot(i.positionX, i.positionY, 'bo', markersize=2)
    else: #exposed
        plt.plot(i.positionX, i.positionY, 'go', markersize=2)
s, e, i, r = ca.sir() #gets current  sir values
plt.subplot(2, 1, 2) # subplot with SEIR
plt.plot(time, susceptible, "b", label="S(t)")
plt.plot(time, exposed, "g", label="E(t)")
plt.plot(time, infected, "r", label="I(t)")
plt.plot(time, removed, "k", label="R(t)")
#plt.legend()
plt.savefig(fname=("plot"+str(len(time))+".png")) #saves figure
filenames.append(("plot"+str(len(time))+".png")) #adds file name to list

infectable = ca.getpossibleinfectable()
infectable = ca.rnginfect(infectable)
ca.appendcells(infectable)

plt.subplot(2,1,1)
for i in ca.cells:
    if i.state == 2: #infected
        plt.plot(i.positionX, i.positionY, 'ro', markersize=2)
    elif i.state == 3: #removed
        plt.plot(i.positionX, i.positionY, 'ko', markersize=2)
    elif i.state == 0: #susceptible
        plt.plot(i.positionX, i.positionY, 'bo', markersize=2)
    else: #exposed
        plt.plot(i.positionX, i.positionY, 'go', markersize=2)
"""
appends new SEIR values to lists
adds time to list
"""
s, e, i, r = ca.sir()
susceptible.append(s/2000)
exposed.append(e/2000)
infected.append(i/2000)
removed.append(r/2000)
time.append(len(time))

plt.subplot(2, 1, 2)
plt.plot(time, susceptible, "b", label="S(t)")
plt.plot(time, exposed, "g", label="E(t)")
plt.plot(time, infected, "r", label="I(t)")
plt.plot(time, removed, "k", label="R(t)")
#plt.legend()
plt.savefig(fname=("plot"+str(len(time))+".png"))
filenames.append(("plot"+str(len(time))+".png"))


are_all_removed = False  # is simulation finished? -> are all removed or no infected & exposed exist
stoprun = 0

"""
with each loop starts next function triggering -> spread of infection
plots current state of environment -> see code above
closes loop when all are infected or none can get infected
"""
while not are_all_removed:
    stoprun += 1
    if stoprun >= 65:
        are_all_removed = True      #stop the simulation after X cyles to not create to many images/ too large gif
    ca.next()
    plt.figure()
    s, e, i, r = ca.sir()
    susceptible.append(s / 2000)
    exposed.append(e / 2000)
    infected.append(i / 2000)
    removed.append(r / 2000)
    time.append(len(time))
    plt.subplot(2, 1, 2)
    plt.plot(time, susceptible,"b", label="S(t)")
    plt.plot(time, exposed,"g", label="E(t)")
    plt.plot(time, infected,"r", label="I(t)")
    plt.plot(time, removed,"k", label="R(t)")
    #plt.legend()
    plt.subplot(2,1,1)
    for i in ca.cells:
        if i.state == 2:
            plt.plot(i.positionX, i.positionY, 'ro', markersize=2)
        elif i.state == 3:
            plt.plot(i.positionX, i.positionY, 'ko', markersize=2)
        elif i.state == 0:
            plt.plot(i.positionX, i.positionY, 'bo', markersize=2)
        else:
            plt.plot(i.positionX, i.positionY, 'go', markersize=2)
    plt.savefig(fname=("plot"+str(len(time))+".png"))
    plt.close()
    filenames.append(("plot" + str(len(time)) + ".png"))

    count = 0 #counts infected
    exposed_or_infected= 0 #count of exposed or infected
    for i in ca.cells:
        if i.state == 3:
            count += 1
        if i.state == 1 or i.state == 2:
            exposed_or_infected +=1
    if count == len(ca.cells): #if all are infected
        are_all_removed = True
    if exposed_or_infected == 0: #if none can get infected
        are_all_removed = True

"""
creates gif from all images
deletes all images afterwards
"""
images = []
for filename in filenames:
    images.append(imageio.imread(filename))
    os.remove(filename)
imageio.mimsave('movie.gif', images)
