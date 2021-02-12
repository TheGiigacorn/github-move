import sys
import pprint

infile =  open(sys.argv[1])
mapsize = (infile.readline())
maprows = mapsize[:mapsize.find(' ')]
mapcols = mapsize[mapsize.find(' ')+1:mapsize.find('\n')]
pacmap = [['' for i in range(int(mapcols))] for j in range(int(maprows))]
pprint.pprint(pacmap)

maprows = int(maprows)
mapcols = int(mapcols)


print(pacmap[0][0])


temp = ''
for i in range(maprows):
    temp += (infile.readline().strip())
    print(temp)


counter = 0
for i in range(maprows):
    for j in range(mapcols):
        pacmap[i][j] = temp[counter]
        counter += 1
pprint.pprint(pacmap)

initdirections = infile.readline()

dunkylocations = infile.readline()

runkylist = infile.readline()

infile.close()




class actman:
    def __init__(self, position):
        self.score = 0
        self.postion = position

class money:
    def __init__(self):
        self.nugget_value = 1
        self.bar_value = 5
        self.diamond_value = 10
        self.nugget_positions = []
        self.bar_positions = []
        self.diamond_positions = []
        self.findMoney()

    def findMoney(self):
        for i in range(maprows):
            for j in range(mapcols):
                if pacmap[i][j] == '.':
                    self.nugget_positions.append([i,j])
                if pacmap[i][j] == '$':
                    self.bar_positions.append([i,j])
                if pacmap[i][j] == '*':
                    self.diamond_positions.append([i,j])



class punky:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

class bunky:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

class dunky:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

class runky:
    def __init__(self, position, direction):
        self.position = position
        self.pointer = 0
        self.direction = direction


    def changePos(self, y, x, money):

        recover = False

        if self.position[0] - y != 0:
            if self.position[0] - y == 1:
                self.direction = 'U'
            if self.position[0] - y == -1:
                self.direction = 'D'
        if self.position[1] - x != 0:
            if self.position[1] - x == 1:
                self.direction = 'L'
            elif self.position[1] - x == -1:
                self.direction = 'R'

        if [self.position[0], self.position[1]] in money.nugget_positions():
            recover = True
            tempy = self.position[0]
            tempx = self.position[1]
        pacmap[self.position[0]][self.position[1]] = ' '
        pacmap[y][x] = 'R'
        self.position[0] = y
        self.position[1] = x
        if recover == True:
            pacmap[tempy][tempx] = '.'

    

    def runkyMove(self, pacmap, movelist, money):

        ################ if runky has 1 possible move ############
        if len(movelist) == 1:
            self.changePos(movelist[0][0], movelist[0][1], money)


        ################# if runky has 2 possible moves ##############
        if len(movelist) == 2:
            if self.direction == 'U':
                if self.position[0] - 1 == movelist[0][0]:
                    movelist.pop(1)
                else:
                    movelist.pop(0)
            if self.direction == 'D':
                if self.position[0] + 1 == movelist[0][0]:
                    movelist.pop(1)
                else:
                    movelist.pop(0)
            if self.direction == 'R':
                if self.position[1] + 1 == movelist[0][1]:
                    movelist.pop(1)
                else:
                    movelist.pop(0)
            if self.direction == 'L':
                if self.position[1] - 1 == movelist[0][1]:
                    movelist.pop(1)
                else:
                    movelist.pop(0)

            self.changePos(movelist[0][0], movelist[0][1], money)


        ################ if runky has 3 possible moves ###############
        if len(movelist) > 2:
            cont = False
            while cont == False:
                if runkylist[self.pointer] == 'U' and self.position[0] - 1 != '#':
                    self.changePos(self.position[0]-1,self.position[1])
                    #pacmap[self.position[0]][self.position[1]] = ' ' 
                    #pacmap[self.position[0]-1][self.position[1]] = 'R'
                    #self.position[0] = self.position[0] - 1
                    self.pointer += 1
                    break
                elif runkylist[self.pointer] == 'R' and self.position[1] + 1 != '#':                
                    self.changePos(self.position[0], self.position[1]+1)
                    self.pointer += 1
                    break
                elif runkylist[self.pointer] == 'D' and self.position[0] + 1 != '#':
                    self.changePos(self.position[0] + 1, self.position[1])
                    self.pointer += 1
                    break
                elif runkylist[self.pointer] == 'L' and self.position[1] - 1 != '#':
                    self.changePost(self.position[0], self.position[1] - 1)
                    self.pointer+= 1
                    break
                else:
                    self.pointer += 1

def main():
    currency = money()
    print(currency.nugget_positions)
    g1 = punky(entityFinder('P'), initdirections[0])
    g2 = punky(entityFinder('B'), initdirections[1])
    g3 = dunky(entityFinder('D'), initdirections[2])
    g4 = runky(entityFinder('R'), initdirections[3])
    act = actman(entityFinder('A'))
    #for i in range(10):
    #punkyMove(actLocate)
    #runkypointer = 0
    for i in range(3):

        g4.runkyMove(pacmap, validMove(entityFinder('R')), currency)
        #print(act.score)
        pprint.pprint(pacmap)



def entityFinder(gamepiece):
    location = ['' for i in range(2)]
    for i in range(maprows):
        for j in range(mapcols):
            if pacmap[i][j] == gamepiece:
                location[0] = i
                location[1] = j
                return location




def validMove(gamepiece):
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
        print('1')
    #right
    if pacmap[gamepiece[0]][gamepiece[1] + 1] != '#':
        tempplace2[0] = gamepiece[0]
        tempplace2[1] = gamepiece[1] + 1
        movelist.append(tempplace2)
        print('2')
    #up
    if pacmap[gamepiece[0] - 1][gamepiece[1]] != '#':
        tempplace3[0] = gamepiece[0] - 1
        tempplace3[1] = gamepiece[1]
        movelist.append(tempplace3)
        print('3')
    #left
    if pacmap[gamepiece[0]][gamepiece[1] - 1] != '#':
        tempplace4[0] = gamepiece[0]
        tempplace4[1] = gamepiece[1] - 1
        movelist.append(tempplace4)
        print('4')
    return movelist

def punkyMove(actman):
    punky = entityFinder('P')
    print(punky)
    moves = validMove(punky)
    print(moves)


'''def BunkyMove()

def DunkyMove()'''

'''def runkyMove(pacmap, pointer):
    print(runkylist)
    runkyloc = entityFinder('R')
    cont = False
    while cont == False:
        if runkylist[pointer] == 'U' and runkyloc[0] - 1 != '#':
            pacmap[runkyloc[0]][runkyloc[1]] = ' ' 
            pacmap[runkyloc[0]-1][runkyloc[1]] = 'R'
            pointer += 1
            break
        elif runkylist[pointer ==''' 
    


main()
