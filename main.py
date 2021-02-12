import sys
import pprint
from math import sqrt
import random


random.seed()

def parseInput():
    infile =  open(sys.argv[1])
    mapsize = (infile.readline())
    maprows = mapsize[:mapsize.find(' ')]
    mapcols = mapsize[mapsize.find(' ')+1:mapsize.find('\n')]
    pacmap = [['' for i in range(int(mapcols))] for j in range(int(maprows))]

    maprows = int(maprows)
    mapcols = int(mapcols)


    temp = ''
    for i in range(maprows):
        temp += (infile.readline().strip())


    counter = 0
    for i in range(maprows):
        for j in range(mapcols):
            pacmap[i][j] = temp[counter]
            counter += 1
    pprint.pprint(pacmap)

    initdirections = infile.readline()

    dunkylocations = infile.readline()
    dunkylist = ['' for i in range(int(dunkylocations[0]))]
    grouper = 2
    for i in range(int(dunkylocations[0])):
        dunkylist[i] = [int(dunkylocations[grouper]),int(dunkylocations[grouper+2])]
        grouper+=4

    runkylist = infile.readline()

    infile.close()
    return pacmap,maprows,mapcols,initdirections,dunkylist,runkylist


class actman:
    def __init__(self, position):
        self.score = 0
        self.position = position
        self.direction = None
        self.movehist = []

    def changePos(self, y, x, pacmap):

        if self.position[0] - y != 0:
            if self.position[0] - y == 1:
                self.movehist.append('U')
                self.direction = 'U'
            elif self.position[0] - y == -1:
                self.movehist.append('D')
                self.direction = 'D'
        if self.position[1] - x != 0:
            if self.position[1] - x == 1:
                self.movehist.append('L')
                self.direction = 'L'
            elif self.position[1] - x == -1:
                self.movehist.append('R')
                self.direction = 'R'

        pacmap[self.position[0]][self.position[1]] = ' '
        pacmap[y][x] = 'A'
        self.position[0] = y
        self.position[1] = x

    def actMove(self, pacmap, movelist):
        move = random.randint(0,1000)%len(movelist)
        self.changePos(movelist[move][0], movelist[move][1], pacmap)

    def moneyGet(self, money):
        if self.position in money.nugget_positions:
            self.score += money.nugget_value
            money.nugget_positions.remove(self.position)
        if self.position in money.bar_positions:
            self.score += money.bar_value
            money.bar_positions.remove(self.position)
        if self.position in money.diamond_positions:
            self.score += money.diamond_value
            money.diamond_positions.remove(self.position)

class money:
    def __init__(self, pacmap, maprows, mapcols):
        self.nugget_value = 1
        self.bar_value = 5
        self.diamond_value = 10
        self.nugget_positions = []
        self.bar_positions = []
        self.diamond_positions = []
        self.findMoney(pacmap,maprows, mapcols)


    #finds all positions of the money/score and puts them in respective lists
    def findMoney(self,pacmap, maprows, mapcols):
        for i in range(maprows):
            for j in range(mapcols):
                if pacmap[i][j] == '.':
                    self.nugget_positions.append([i,j])
                if pacmap[i][j] == '$':
                    self.bar_positions.append([i,j])
                if pacmap[i][j] == '*':
                    self.diamond_positions.append([i,j])

    #function that restores money that ghosts have walked over                
    def restoreMoney(self, maprows, mapcols,pacmap):
        entitystr = ['A','P','B','D','R']
        for i in range(maprows):
            for j in range(mapcols):

                ##### restores dots/nuggets that act man has not collected #####
                for k in range(len(self.nugget_positions)):
                    if self.nugget_positions[k][0] == i and self.nugget_positions[k][1] == j and pacmap[i][j] not in entitystr:
                        pacmap[i][j] = '.'

                #### restores dollars/bars that act man has not collected #####
                for l in range(len(self.bar_positions)):
                    if self.bar_positions[l][0] == i and self.bar_positions[l][1] == j and pacmap[i][j] not in entitystr:
                        pacmap[i][j] = '$'

                #### restores stars/diamonds that act man has not collected ######
                for m in range(len(self.diamond_positions)):
                    if self.diamond_positions[m][0] == i and self.diamond_positions[m][1] == j and pacmap[i][j] not in entitystr:

                        pacmap[i][j] = '*'




class punky:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction


    def changePos(self, y, x, pacmap):

        if self.position[0] - y != 0:
            if self.position[0] - y == 1:
                self.direction = 'U'
            elif self.position[0] - y == -1:
                self.direction = 'D'
        if self.position[1] - x != 0:
            if self.position[1] - x == 1:
                self.direction = 'L'
            elif self.position[1] - x == -1:
                self.direction = 'R'

        pacmap[self.position[0]][self.position[1]] = ' '
        pacmap[y][x] = 'P'
        self.position[0] = y
        self.position[1] = x

    def punkyMove(self, pacmap, movelist, actpos):
         ################ if punky has 1 possible move ############
        if len(movelist) == 1:
            self.changePos(movelist[0][0], movelist[0][1], pacmap)


        ################# if punky has 2 possible moves ##############
        if len(movelist) == 2:
            movelist = twoPossibleMoves(self.position, self.direction, movelist)

            self.changePos(movelist[0][0], movelist[0][1], pacmap)

        ############## if punky has 3 or more moves #############
        if len(movelist) > 2:
            mindistance = 999
            minindex = -1
            for i in range(len(movelist)):
                distance = sqrt(((movelist[i][0] - actpos[0]) ** 2) + ((movelist[i][1] -  actpos[1]) ** 2))
                if distance < mindistance:
                    minindex = i
                    mindistance = distance
            self.changePos(movelist[minindex][0], movelist[minindex][1], pacmap)

                
class bunky:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def changePos(self, y, x, pacmap):

        if self.position[0] - y != 0:
            if self.position[0] - y == 1:
                self.direction = 'U'
            elif self.position[0] - y == -1:
                self.direction = 'D'
        if self.position[1] - x != 0:
            if self.position[1] - x == 1:
                self.direction = 'L'
            elif self.position[1] - x == -1:
                self.direction = 'R'

        pacmap[self.position[0]][self.position[1]] = ' '
        pacmap[y][x] = 'B'
        self.position[0] = y
        self.position[1] = x

    def bunkyMove(self, pacmap, movelist, actpos, actdir):
         ################ if bunky has 1 possible move ############
        if len(movelist) == 1:
            self.changePos(movelist[0][0], movelist[0][1], pacmap)


        ################# if bunky has 2 possible moves ##############
        if len(movelist) == 2:
            movelist = twoPossibleMoves(self.position, self.direction, movelist)

            self.changePos(movelist[0][0], movelist[0][1], pacmap)
        ############## if bunky has 3 or more possible moves ##########
        if len(movelist) > 2:

            if actdir == 'U':
                movey = actpos[0] - 4
                movex = actpos[1]
            if actdir == 'R':
                movey = actpos[0]
                movex = actpos[1] + 4
            if actdir == 'D':
                movey = actpos[0] + 4
                movex = actpos[1]
            if actdir == 'L':
                movey = actpos[0]
                movex = actpos[1] - 4

            mindistance = 999
            minindex = -1
            for i in range(len(movelist)):
                distance = sqrt(((movelist[i][0] - movey) ** 2) + ((movelist[i][1] - movex) ** 2))
                if distance < mindistance:
                    minindex = i
                    mindistance = distance
            self.changePos(movelist[minindex][0], movelist[minindex][1], pacmap)
            



class dunky:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.pointer = 0

    def changePos(self, y, x, pacmap):

        if self.position[0] - y != 0:
            if self.position[0] - y == 1:
                self.direction = 'U'
            elif self.position[0] - y == -1:
                self.direction = 'D'
        if self.position[1] - x != 0:
            if self.position[1] - x == 1:
                self.direction = 'L'
            elif self.position[1] - x == -1:
                self.direction = 'R'

        pacmap[self.position[0]][self.position[1]] = ' '
        pacmap[y][x] = 'D'
        self.position[0] = y
        self.position[1] = x

    

    def dunkyMove(self, pacmap, movelist, dunkylist):
        if self.position in dunkylist:
            self.pointer += 1
            if self.pointer >= len(dunkylist):
                self.pointer = 0

        ################ if dunky has 1 possible move ############
        if len(movelist) == 1:
            self.changePos(movelist[0][0], movelist[0][1],pacmap)


        ################# if dunky has 2 possible moves ##############
        if len(movelist) == 2:
            movelist = twoPossibleMoves(self.position, self.direction, movelist)

            self.changePos(movelist[0][0], movelist[0][1],pacmap)

        ################ if dunky has more than 2 possible moves ###########
        if len(movelist) > 2:
            targety = dunkylist[self.pointer][0]
            targetx = dunkylist[self.pointer][1]

            mindistance = 999
            minindex = -1
            for i in range(len(movelist)):
                distance = sqrt(((movelist[i][0] - int(targety)) ** 2) + ((movelist[i][1] - int(targetx)) ** 2))
                if distance < mindistance:
                    minindex = i
                    mindistance = distance
            self.changePos(movelist[minindex][0], movelist[minindex][1],pacmap)



        
class runky:
    def __init__(self, position, direction):
        self.position = position
        self.pointer = 0
        self.direction = direction


    def changePos(self, y, x, pacmap):

        if self.position[0] - y != 0:
            if self.position[0] - y == 1:
                self.direction = 'U'
            elif self.position[0] - y == -1:
                self.direction = 'D'
        if self.position[1] - x != 0:
            if self.position[1] - x == 1:
                self.direction = 'L'
            elif self.position[1] - x == -1:
                self.direction = 'R'

        pacmap[self.position[0]][self.position[1]] = ' '
        pacmap[y][x] = 'R'
        self.position[0] = y
        self.position[1] = x

    

    def runkyMove(self, pacmap, movelist, runkylist):

        ################ if runky has 1 possible move ############
        if len(movelist) == 1:
            self.changePos(movelist[0][0], movelist[0][1], pacmap)


        ################# if runky has 2 possible moves ##############
        if len(movelist) == 2:
            movelist = twoPossibleMoves(self.position, self.direction, movelist)

            self.changePos(movelist[0][0], movelist[0][1], pacmap)


        ################ if runky has 3 possible moves ###############
        if len(movelist) > 2:
            cont = False
            while cont == False:
                if runkylist[self.pointer] == 'U' and self.position[0] - 1 != '#':
                    self.changePos(self.position[0]-1,self.position[1],pacmap)
                    self.pointer += 1
                    break
                elif runkylist[self.pointer] == 'R' and self.position[1] + 1 != '#':                
                    self.changePos(self.position[0], self.position[1]+1,pacmap)
                    self.pointer += 1
                    break
                elif runkylist[self.pointer] == 'D' and self.position[0] + 1 != '#':
                    self.changePos(self.position[0] + 1, self.position[1],pacmap)
                    self.pointer += 1
                    break
                elif runkylist[self.pointer] == 'L' and self.position[1] - 1 != '#':
                    self.changePos(self.position[0], self.position[1] - 1, pacmap)
                    self.pointer+= 1
                    break
                else:
                    self.pointer += 1
                if self.pointer >= len(runkylist):
                    self.pointer = 0

def main():
    pacmap, maprows, mapcols, initdirections, dunkylist, runkylist = parseInput()
    currency = money(pacmap, maprows, mapcols)
    g1 = punky(entityFinder('P',maprows,mapcols,pacmap), initdirections[0])
    g2 = bunky(entityFinder('B',maprows,mapcols,pacmap), initdirections[1])
    g3 = dunky(entityFinder('D',maprows,mapcols,pacmap), initdirections[2])
    g4 = runky(entityFinder('R',maprows,mapcols,pacmap), initdirections[3])
    act = actman(entityFinder('A',maprows,mapcols,pacmap))
    #pacmap[2][2] = ' '
    #pacmap[1][4] = ' '
    #pacmap[3][4] = ' '
    #pacmap[2][6] = ' '
    #pacmap[2][7] = ' '
    #pacmap[2][8] = ' '
    for i in range(20):
        #act man moves here
        act.actMove(pacmap, validMove(act.position,pacmap))

        #checks to see if act man ran into a ghost
        if pacGhostCollision(pacmap,act,g1,g2,g3,g4):
            break

        #all the ghosts move in order
        g1.punkyMove(pacmap, validMove(g1.position,pacmap), act.position)
        g2.bunkyMove(pacmap, validMove(g2.position,pacmap), act.position, act.direction)
        g3.dunkyMove(pacmap, validMove(g3.position,pacmap), dunkylist)
        g4.runkyMove(pacmap, validMove(g4.position,pacmap), runkylist)

        print(g2.position)

        #checks to see if the ghosts ran into actman
        if pacGhostCollision(pacmap,act,g1,g2,g3,g4):
            break

        act.moneyGet(currency) 

        #print(act.score)

        #this function call restores all money that the ghosts have walked over
        currency.restoreMoney(maprows,mapcols,pacmap)
        printPacMap(pacmap, maprows, mapcols)
    print(''.join(act.movehist))
    print(act.score)
    printPacMap(pacmap, maprows,mapcols)


def printPacMap(pacmap, maprows, mapcols):
    for i in range(maprows):
        if i > 0:
            print('\r')
        for j in range(mapcols):
            print(pacmap[i][j],end='')
    print('\r')

def pacGhostCollision(pacmap, act, punky, bunky, dunky, runky):
    if act.position == punky.position or act.position == bunky.position or act.position == dunky.position or act.position == runky.position:
        pacmap[act.position[0]][act.position[1]] = 'X'
        return True

def twoPossibleMoves(position, direction, movelist):
    if direction == 'U':
        #and object has up in the first index of possible moves
        if position[0] - 1 == movelist[0][0]:
            movelist.pop(1)
        #and object has up in the second index of possible moves
        elif position[0] - 1 == movelist[1][0]:
            movelist.pop(0)
        elif position[0] + 1 == movelist[0][0]:
            movelist.pop(0)
        else:
            movelist.pop(1)


    if direction == 'D':
        #and object has down in the first index of possible moves
        if position[0] + 1 == movelist[0][0]:
            movelist.pop(1)
        #and object has down in the second index of possible moves
        elif position[0] + 1 == movelist[1][0]:
            movelist.pop(0)
        elif position[0] - 1 == movelist[0][0]:
            movelist.pop(0)
        else:
            movelist.pop(1)


    if direction == 'R':
        #and object has right in the first index of possible moves
        if position[1] + 1 == movelist[0][1]:
            movelist.pop(1)
        #and object has right in the second index of possible moves
        elif position[1] + 1 == movelist[1][1]:
            movelist.pop(0)
        #if possible direction is left
        elif position[1] - 1 == movelist[0][1]:
            movelist.pop(0)
        else:
            movelist.pop(1)


    #when objects direction is left        
    if direction == 'L':
        #and object has left in the first index of possible moves
        if position[1] - 1 == movelist[0][1]:
            movelist.pop(1)
        #and object has left in the second index of possible moves
        elif position[1] - 1 == movelist[1][1]:
            movelist.pop(0)
        #if possible direction is right
        elif position[1] + 1 == movelist[0][1]:
            movelist.pop(0)
        else:
            movelist.pop(1)
    return movelist



def entityFinder(gamepiece, maprows, mapcols,pacmap):
    location = ['' for i in range(2)]
    for i in range(maprows):
        for j in range(mapcols):
            if pacmap[i][j] == gamepiece:
                location[0] = i
                location[1] = j
                return location


def validMove(gamepiece,pacmap):
    movelist = []
    tempplace1 = ['' for i in range(2)]
    tempplace2 = ['' for i in range(2)]
    tempplace3 = ['' for i in range(2)]
    tempplace4 = ['' for i in range(2)]

    #down
    if pacmap[gamepiece[0] + 1][gamepiece[1]] != '#':
        tempplace1[0] = gamepiece[0] + 1
        tempplace1[1] = gamepiece[1]
        movelist.append(tempplace1)
        #print('1')
    #right
    if pacmap[gamepiece[0]][gamepiece[1] + 1] != '#':
        tempplace2[0] = gamepiece[0]
        tempplace2[1] = gamepiece[1] + 1
        movelist.append(tempplace2)
        #print('2')
    #up
    if pacmap[gamepiece[0] - 1][gamepiece[1]] != '#':
        tempplace3[0] = gamepiece[0] - 1
        tempplace3[1] = gamepiece[1]
        movelist.append(tempplace3)
        #print('3')
    #left
    if pacmap[gamepiece[0]][gamepiece[1] - 1] != '#':
        tempplace4[0] = gamepiece[0]
        tempplace4[1] = gamepiece[1] - 1
        movelist.append(tempplace4)
        #print('4')
    return movelist

    


main()
