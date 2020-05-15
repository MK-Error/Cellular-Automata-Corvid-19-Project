import numpy as np

from Cell import Cell


class CellularAutomaton:
    
    """
    constructor of class: param -> SEIR data, infection rate , incubation periode, latent time , spread range
    movement possibility and move distance
    creates list of cells with full population
    created infected cells in cells list by changing state
    """
    def __init__(self, susceptible, exposed, infected, removed,infection_rate,incubation_period,latent_time,spreadrange,ismoving,movedistance):
        self.susceptible = susceptible
        self.infected = infected
        self.removed = removed
        self.exposed = exposed
        self.infection_rate = infection_rate
        self.incubation_period = incubation_period
        self.latent_time = latent_time
        self.population = susceptible+infected+removed+exposed
        self.cells = [Cell() for i in range(self.population)]

        for i in range(infected):
            self.cells[i].state = 2
        self.environment = spreadrange
        self.ismoving = ismoving
        self.movedistance = movedistance

    """
    getpossibleinfectable function: gets all infectable cells from cells list
    all infected are poped from cells list and added to separate list (infectedlist)
    -> nested loop goes through all infected and checks is other susceptible cells
    are in range to be infected
    -> susceptible cells are than pop from list and added to separate list (infectable)
    -> calls appendcells to append infected back into cells list 
    -> returns list of susceptible
    """
    def getpossibleinfectable(self):
        infectable = []
        infectedlist = []
        counter = 0
        while counter != len(self.cells):
            if self.cells[counter].state == 2:
                infectedlist.append(self.cells.pop(counter))
            else:
                counter += 1
        counter = 0
        for i in infectedlist:
            while counter != len(self.cells):
                x = self.cells[counter].positionX
                y = self.cells[counter].positionY
                #checks bounds of infection radius
                if  x >= i.positionX - self.environment and x <= i.positionX + self.environment and y >= i.positionY - self.environment and y <= i.positionY + self.environment  and self.cells[counter].state==0:
                    infectable.append(self.cells.pop(counter))
                else:
                    counter += 1
            counter=0
        self.appendcells(infectedlist)
        return infectable

    """
    rnginfect function: tries to infect cell
    random number is generated between 0 and 1 -> if number smaller than infection rate
    -> cell gets infected
    returns cell list
    """
    def rnginfect(self, cells):
        for i in cells:
            if np.random.uniform() < self.infection_rate:
                i.state = 1

        return cells

    """
    changestate function: iterates through cells list and updates state of cells
    if time since infection or exposure is equals to limit -> incubation periode & latent time 
    -> change state of cell accordingly
    """
    def changestate(self):
        for i in self.cells:
            if i.state == 1 or i.state == 2:
                i.time_since_infection +=1
                if i.state == 1 and i.time_since_infection == self.incubation_period:
                    i.state = 2
                    i.time_since_infection=0
                if i.state == 2 and i.time_since_infection == self.latent_time:
                    i.state = 3

    """
    appendcells function: appends list of cells into main cell list
    mainly used to append infectable cells
    """
    def appendcells(self,cells):
        for i in cells:
            self.cells.append(i)

    """
    movecells function: tries to move cells in X and Y direction
    creates random number between 0 and 1 and compares to move probability (ismoving)
    in case the cell is moving the distance in X and Y direction is created by a random number between
    negative and positive move distance -> number is then added to current position
    checks if in bounds of [100x100] -> sets position to boundary if not in range 
    """
    def movecells(self):

        for i in self.cells:
            if np.random.uniform() < self.ismoving:
                i.positionY += np.random.randint(-self.movedistance, self.movedistance)
                if i.positionY > 200:
                    i.positionY = 200
                if i.positionY < 0:
                    i.positionY = 0
                i.positionX += np.random.randint(-self.movedistance, self.movedistance)
                if i.positionX > 200:
                    i.positionX = 200
                if i.positionX < 0:
                    i.positionX = 0

    """
    sir function: returns current state of population -> Susceptible, exposed, infected,removed
    iterates through cells to find state and count all states in SEIR groups
    """
    def sir(self):
        s=0
        e=0
        inf=0
        r=0
        for i in self.cells:
            if i.state == 0:
                s += 1
            if i.state == 1:
                e += 1
            if i.state == 2:
                inf += 1
            if i.state == 3:
                r += 1
        return s, e, inf, r

    """
    next function: triggers all functions necessary for next step in time
    changes states of cells -> moves cells -> gets infectable population -> tries to infect 
    -> adds infectable population back to main population
    """
    def next(self):
        self.changestate()
        self.movecells()
        infectable = self.getpossibleinfectable()
        infectable = self.rnginfect(infectable)
        self.appendcells(infectable)
