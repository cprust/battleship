#Author: Chris Prust
#2015

import sys
import random
import time

#execfile("battleField.py")
class Carrier(object):
    
    def __init__(self,name):
        self.name = name
        self.health = 100
        self.speed = 1
        self.radar = 10
        self.position = []

class Destroyer(object):

    def __init__(self,name):
        self.name = name
        self.health = 60
        self.speed = 2
        self.radar = 5
        self.position = []
        self.ASM = 6 #anti-ship missle
        self.HARM = 2 #high speed anti radar missle
        self.SRM = 6#short range missle

class Patrol(object):
    
    def __init__(self,name):
        self.name = name
        self.health = 30
        self.speed = 4
        self.radar = 3
        self.position = []
            

class Game(object):

    def __init__(self):
        self.currentPlayer = 1 #1 or 2
        self.player1Ships = []
        self.player2Ships = []
        self.player1DeadShips = []
        self.player2DeadShips = []
        self.player1History = []#history of where enemy ships have been on player 1 screen
        self.player2History = []#history of where enemy ships have been on player 2 screen
        self.endgame = 0#0 or 1
        self.points = 7.0
        self.sizeFieldx = 51
        self.sizeFieldy = 52
        self.allStartPositions = []#lists all positions of all ships
        self.ASMflag = 0
        self.ASMposition = []
        self.ASMfixedDamage = 20 
        self.ASMvariableDamage = 20 
        self.SRMfixedDamage = 10
        self.SRMvariableDamage = 10 
        self.HARMfixedDamage = 20 
        self.HARMvariableDamage = 20
        self.PlanesfixedDamage = 30
        self.PlanesvariableDamage = 20 
        self.ASMrange = 30 
        self.SRMrange = 8
        self.HARMrange = 15
        self.Planesrange = 6 
        self.ASMpoints = 2.0
        self.SRMpoints = 1.25
        self.HARMpoints = 4.0
        self.Planespoints = 2.0
        self.numGuesses = 0#so people don't just cheat
        self.middleLine = 26#dividing line that seperates player1 from player2 at beginning of game -- used in printEmptyField() and printField()

    def checkPoints(self,pointsUsed):
        #checks if there are enough point to complete task, (but does not deduct them)
        #returns either True or False
        if((self.points-abs(pointsUsed)) >= 0):
            return True
        else:
            return False

    def checkShip(self,shipName,player):
        #checks if a ship exists and returns True if it does
        if(player == "Player1"):
            for x in range(0,len(self.player1Ships)):
                if(shipName == self.player1Ships[x].name):
                    return True
        else:
            for x in range(0,len(self.player2Ships)):
                if(shipName == self.player2Ships[x].name):
                    return True
        return False#if it hasn't returned yet

    def checkinBounds(self,list):
        #checks if a list's values are inbounds and valid and returns True or False
        for x in range(0,len(list)):
            if(not(isinstance(list[x][0],(int,long)) and isinstance(list[x][1],(int,long)) and list[x][0]>=0 and list[x][0]<=self.sizeFieldx-1 and list[x][1]>=0 and list[x][1]<=self.sizeFieldy-1)):
                return False
        else:
            return True

    def checkRotation(self,rotation):
        #checks if rotation is between 0 and 360 and a multiple of 45 and then returns True or False
        if(not isinstance(rotation, (int, long))):
            return False
        if(rotation>=0 and rotation<=360 and rotation%45 == 0):
            return True
        else:
            return False
    
    def printEmptyField(self):
        #This just prints an empty field at the beginning of the game

        middleLine = self.middleLine
        field =[[0 for j in range(self.sizeFieldx)] for i in range(self.sizeFieldy)]

        for y in range (0,self.sizeFieldy):
            for x in range (0,self.sizeFieldx):
                field[y][x] = x
            #print x
        yAxisPlaceHolders = [0 for i in range(self.sizeFieldy)]
        for y in range(0,self.sizeFieldy):
            yAxisPlaceHolders[y] = y
        #print yAxisPlaceHolders[y]
    #print field
        for y in range (0,self.sizeFieldy):
            if(y<10):
                print str(yAxisPlaceHolders[y])+"||",
            else:
                print str(yAxisPlaceHolders[y])+"|",
            for x in range(0,self.sizeFieldx):
                if(x < self.sizeFieldx-1 and not isinstance(field[y][x],basestring) and (field[y][x] != middleLine)):
                    print str(field[y][x]),
                elif(x < self.sizeFieldx-1 and not isinstance(field[y][x],basestring) and (field[y][x] == middleLine)):
                    print '\033[95m' + str(field[y][x]) + '\033[0m',#prints middle line in different color
                elif(x < self.sizeFieldx-1 and isinstance(field[y][x],basestring) and (field[y][x] != middleLine)):
                    print str(field[y][x]),
                elif(x < self.sizeFieldx-1 and isinstance(field[y][x],basestring) and (field[y][x] == middleLine)):
                    print '\033[95m' + str(field[y][x]) + '\033[0m',#prints middle line in different color
                else:
                    print str(field[y][x])
                    
    def checkAdjointInput(self,list):
        #This function checks if user input makes ships adjoint. Returns True or False
        #Input must be in a vertical or horizontal line. no diagonal.
        
        if (len(list) == 1):
            return True
        elif(list[0][0]==list[1][0]):#if x is the same in y direction -- vertical
            for x in range(0,len(list)-1):#check that x is the same
                if(list[x][0] != list[x+1][0]):
                    return False
            for x in range(0,len(list)-1):#check that y increases only by one
                if(abs(list[x][1]-list[x+1][1]) != 1):
                    return False
            return True
        
        #Check to make sure symmetry is good
        elif(list[0][1]==list[1][1]):#if y is the same in x direction -- horizontal
            for x in range(0,len(list)-1):#check that y is the same
                if(list[x][1] != list[x+1][1]):
                    return False
            for x in range(0,len(list)-1):#check that x increases only by one
                if(abs(list[x][0]-list[x+1][0]) != 1):
                    return False
            return True
        else:
            return False
    
    def shipUserInput(self,shipname,player):
        #Reads input from user
        while True:
            try:
                carrierPos = raw_input(player + " "+"\033[1;47;30mEnter position of\033[0m"+" " + shipname + ": ")
                while(len(carrierPos) == 0):
                    print "Input not Valid! Reenter information."
                    carrierPos = raw_input(player + " "+"\033[1;47;30mEnter position of\033[0m"+" " + shipname + ": ")
                numbers = map(int, carrierPos.split())
                for x in range(0,len(numbers)):
                    numbers[x] = int(numbers[x])
                return numbers
            except ValueError:
                print("Input not Valid! Reenter information.")
    
    def makeUserInput2DList(self,list,shipname,player):
        #takes the user input and makes it into a 2D list
        sizeof2DList = int(len(list)/2)
        newList = list
        if(len(list)%2 != 0):
            print "Uneven amount of enteries. Enter Valid Input."
            newList = self.shipUserInput(shipname,player)
            sizeof2DList = int(len(newList)/2)
            while(len(newList)%2 != 0):
                print "Uneven amount of enteries. Enter Valid Input."
                newList = self.shipUserInput(shipname,player)
                sizeof2DList = int(len(newList)/2)
        position = [[0 for j in range(2)] for i in range(sizeof2DList)]
        for x in range(0,len(newList)):
            if(x%2 != 0):
                xory = 1#y
            else:
                xory = 0#x
            position[int(x/2)][xory] = newList[x]
            #print x/2
        return position

    def startIntersection(self,list):
        #Tells if there are intersections
        allStartPositions = self.allStartPositions
        for x in range(0,len(list)):
            for y in range(0,len(allStartPositions)):
                if(list[x] == allStartPositions[y]):
                    return False
        return True

    def masterInput(self,shipname,player,typeShip):
        #calls on lower level input functions

        middleLine = self.middleLine
        if(player == "Player1"):
            self.currentPlayer = 1
        else:
            self.currentPlayer = 2
        allStartPositions = self.allStartPositions
        #master function that runs all input
        sizeShip = 0
        if(typeShip == "carrier"):
            sizeShip = 5
        elif(typeShip == "destroyer"):
            sizeShip = 3
        else:
            sizeShip = 1
        pos = self.shipUserInput(shipname,player)
        #print "here"
        position = self.makeUserInput2DList(pos,shipname,player)
        
        
        if(player == "Player1"):#make sure x input is less than middleLine
            flag = 0
            while(True):
                for x in range(0,len(position)):
                    if(position[x][0] >= middleLine):
                        flag = 1#raise flag
                        print "Player1 must place ships to the left of the middle line."
                        break
                if(flag == 0):
                    break
                else:#(flag == 1):
                    flag = 0#reset flag
                    pos = self.shipUserInput(shipname,player)
                    position = self.makeUserInput2DList(pos,shipname,player)

        else: #(player == "Player2"): #make sure x input is greater than middleLine
            flag = 0
            while(True):
                for x in range(0,len(position)):
                    if(position[x][0] <= middleLine):
                        flag = 1#raise flag
                        print "Player2 must place ships to the right of the middle line."
                        break
                if(flag == 0):
                    break
                else:#(flag == 1):
                    flag = 0#reset flag
                    pos = self.shipUserInput(shipname,player)
                    position = self.makeUserInput2DList(pos,shipname,player)
        
            
        while(not self.checkAdjointInput(position) or not self.checkinBounds(position) or sizeShip != len(position) or not self.startIntersection(position)):
            print "The value inputted are not adjoint, vertical, horizontal, in bounds, correctly sized, or intersects another ship."
            print "Reenter Valid Input."
            pos = self.shipUserInput(shipname,player)
            #print "here1"
            position = self.makeUserInput2DList(pos,shipname,player)
        for x in range(0,len(position)):
            self.allStartPositions.append(position[x])
        return position

    def printField(self, player):
        #Will print the field of the player
        
        middleLine = self.middleLine
        for x in range(0,10):#print extra spaces
            print " "
        field =[[0 for j in range(self.sizeFieldx)] for i in range(self.sizeFieldy)]
        #'\003'+"1"
        for y in range (0,self.sizeFieldy):
            for x in range (0,self.sizeFieldx):
                field[y][x] = x
        if(player == "Player1"):
            carrierSym = '\033[94m'
            destroyerSym ='\033[94m'
            patrolSym = '\033[94m'
            endSym = '\033[0m'
            for x in range(0,len(self.player1Ships)):
                if(len(self.player1Ships[x].position) != 0):
                    for y in range(0,len(self.player1Ships[x].position)):
                        if(type(self.player1Ships[x]) is Carrier):
                            symbol = carrierSym
                        elif(type(self.player1Ships[x]) is Destroyer):
                            symbol = destroyerSym
                        else:
                            symbol = patrolSym
                        #print self.allStartPositions
                        field[self.player1Ships[x].position[y][1]][self.player1Ships[x].position[y][0]] = symbol+self.player1Ships[x].name+endSym
        
        else:#Player2
            carrierSym = '\033[94m'
            destroyerSym ='\033[94m'
            patrolSym = '\033[94m'
            endSym = '\033[0m'
            for x in range(0,len(self.player2Ships)):
                if(len(self.player2Ships[x].position) != 0):
                    for y in range(0,len(self.player2Ships[x].position)):
                        if(type(self.player2Ships[x]) is Carrier):
                            symbol = carrierSym
                        elif(type(self.player2Ships[x]) is Destroyer):
                            symbol = destroyerSym
                        else:
                            symbol = patrolSym
                        field[self.player2Ships[x].position[y][1]][self.player2Ships[x].position[y][0]] = symbol+self.player2Ships[x].name+endSym
        
        yAxisPlaceHolders = [0 for i in range(self.sizeFieldy)]
        for y in range(0,self.sizeFieldy):
            yAxisPlaceHolders[y] = y
        for y in range (0,self.sizeFieldy):
            if(y<10):
                print str(yAxisPlaceHolders[y])+"||",
            else:
                print str(yAxisPlaceHolders[y])+"|",
            for x in range(0,self.sizeFieldx):
                if(x < self.sizeFieldx-1 and not isinstance(field[y][x],basestring) and (field[y][x] != middleLine)):
                    if(x<10):
                        print str(field[y][x])+"|",
                    else:
                        print str(field[y][x]),
                elif(x < self.sizeFieldx-1 and not isinstance(field[y][x],basestring) and (field[y][x] == middleLine)):
                    if(x<10):
                        print '\033[95m' + str(field[y][x])+"|" + '\033[0m',#print middle line in different color
                    else:
                        print '\033[95m' + str(field[y][x]) + '\033[0m',#print middle line in different color
                elif(x < self.sizeFieldx-1 and isinstance(field[y][x],basestring)):
                    print str(field[y][x]),
                else:
                    print str(field[y][x])
    
    def findandreplace(self,oldPosition,newPosition):
        #replaces old position in self.allStartPositions with new position
        for x in range(0,len(oldPosition)):
            self.allStartPositions.remove(oldPosition[x])
        for x in range(0,len(newPosition)):
            self.allStartPositions.append(newPosition[x])
    
    def removefromlist(self,list):
        #remove value of list from self.allStartPositions if it exists in the list
        for x in range(0,len(list)):
            if(list[x] in self.allStartPositions):
                self.allStartPositions.remove(list[x])
    
    def addtolist(self,list):
        #add value of list from self.allStartPositions if it is not already present
        for x in range(0,len(list)):
            if(not list[x] in self.allStartPositions):
                self.allStartPositions.append(list[x])
    
    def findcourse(self,player,shipName):
        #finds the current course of the ship

        currCourse = 0
        if(not self.checkShip(shipName,player)):
            return False

        if(player == "Player1"):
            x = 0
            while(shipName != self.player1Ships[x].name):
                x = x + 1
            highestx=self.player1Ships[x].position[0][0]
            placeofHighestx = 0
            for y in range(0,len(self.player1Ships[x].position)):#find highest x
                if(self.player1Ships[x].position[y][0]>highestx):
                    highesty = self.player1Ships[x].position[y][0]
                    placeofHighestx = y
            lowesty = self.player1Ships[x].position[0][1]
            for y in range(0,len(self.player1Ships[x].position)):#find lowest y                                                                                                                     
                if(self.player1Ships[x].position[y][1]<lowesty):
                    lowesty = self.player1Ships[x].position[y][1]
            if(self.player1Ships[x].position[0][0] == self.player1Ships[x].position[len(self.player1Ships[x].position)-1][0]):#same x so course 0
                currCourse = 0
                return currCourse
            elif(self.player1Ships[x].position[0][1] == self.player1Ships[x].position[len(self.player1Ships[x].position)-1][1]):#same y so course 90
                currCourse = 90
                return currCourse
            elif(self.player1Ships[x].position[placeofHighestx][1] == lowesty):#if highest x paired with lowest y course 45
                currCourse = 45
                return currCourse
            else:
                currCourse = 135
                return currCourse
            
        else:
            x = 0
            while(shipName != self.player2Ships[x].name):
                x = x + 1
            highestx=self.player2Ships[x].position[0][0]
            placeofHighestx = 0
            for y in range(0,len(self.player2Ships[x].position)):#find highest x
                if(self.player2Ships[x].position[y][0]>highestx):
                    highesty = self.player2Ships[x].position[y][0]
                    placeofHighestx = y
            lowesty = self.player2Ships[x].position[0][1]
            for y in range(0,len(self.player2Ships[x].position)):#find lowest y                                                                                                                     
                if(self.player2Ships[x].position[y][1]<lowesty):
                    lowesty = self.player2Ships[x].position[y][1]
            if(self.player2Ships[x].position[0][0] == self.player2Ships[x].position[len(self.player2Ships[x].position)-1][0]):#same x so course 0
                currCourse = 0
                return currCourse
            elif(self.player2Ships[x].position[0][1] == self.player2Ships[x].position[len(self.player2Ships[x].position)-1][1]):#same y so course 90
                currCourse = 90
                return currCourse
            elif(self.player2Ships[x].position[placeofHighestx][1] == lowesty):#if highest x paired with lowest y course 45
                currCourse = 45
                return currCourse
            else:
                currCourse = 135
                return currCourse

    def cometocourse(self,player,shipName,course):
        #changes course of ship
        
        if(self.checkRotation(course) and self.checkShip(shipName,player)):
            x = 0
            if(player == "Player1"):
                while(shipName != self.player1Ships[x].name):
                    x = x + 1
                currentPos = self.player1Ships[x].position
                if(type(self.player1Ships[x]) is Patrol):#Patrol Can't change course, only one square.#################NEED TO CHECK
                    print "Patrol can't come to course"
                    return False
                #determining the current course
                currCourse = self.findcourse(player,shipName)

                #Determining new positions based on new course
                newPos = []#position after rotation
                if(len(self.player1Ships[x].position) == 3):#its a destroyer
                    if(course == 0 or course == 180):
                        factor = 1
                        for y in range(0,len(self.player1Ships[x].position)):
                            newPos.append([self.player1Ships[x].position[1][0],((self.player1Ships[x].position[1][1])-factor)])
                            factor = factor - 1
                    elif(course == 45 or course == 225):
                        factor = 1
                        for y in range(0,len(self.player1Ships[x].position)):
                            newPos.append([((self.player1Ships[x].position[1][0])-factor),((self.player1Ships[x].position[1][1])+factor)])
                            factor = factor - 1
                    elif(course == 90 or course == 270):
                        factor = 1
                        for y in range(0,len(self.player1Ships[x].position)):
                            newPos.append([((self.player1Ships[x].position[1][0])-factor),((self.player1Ships[x].position[1][1]))])
                            factor = factor - 1
                    else:#135 or 315
                        factor = 1
                        for y in range(0,len(self.player1Ships[x].position)):
                            newPos.append([((self.player1Ships[x].position[1][0])-factor),((self.player1Ships[x].position[1][1])-factor)])
                            factor = factor - 1
                            
                else:#its a carrier
                    if(course == 0 or course == 180):
                        factor = 2
                        for y in range(0,len(self.player1Ships[x].position)):
                            newPos.append([self.player1Ships[x].position[2][0],((self.player1Ships[x].position[2][1])-factor)])
                            factor = factor - 1
                    elif(course == 45 or course == 225):
                        factor = 2
                        for y in range(0,len(self.player1Ships[x].position)):
                            newPos.append([((self.player1Ships[x].position[2][0])-factor),((self.player1Ships[x].position[2][1])+factor)])
                            factor = factor - 1
                    elif(course == 90 or course == 270):
                        factor = 2
                        for y in range(0,len(self.player1Ships[x].position)):
                            newPos.append([((self.player1Ships[x].position[2][0])-factor),((self.player1Ships[x].position[2][1]))])
                            factor = factor - 1
                    else:#135 or 315
                        factor = 2
                        for y in range(0,len(self.player1Ships[x].position)):
                            newPos.append([((self.player1Ships[x].position[2][0])-factor),((self.player1Ships[x].position[2][1])-factor)])
                            factor = factor - 1
                
                #Find how many points it takes to turn
                if(course == 0 or course==180):
                    abscourse = 0
                elif(course == 45 or course==225):
                    abscourse = 45
                elif(course == 90 or course==270):
                    abscourse = 90
                else:
                    abscourse = 135
                numRot = abs(currCourse - abscourse)/45#number of rotations

                if(numRot == 3):#because could always just turn the other way
                    numRot = 1

                if(len(self.player1Ships[x].position) == 3):
                    numPoints = numRot #number of points to turn destroyer
                else:
                    numPoints = numRot * 2 #x2 points to turn carrier
                
                self.removefromlist(self.player1Ships[x].position)#removing old values so that there will be no intersections
        
                #print self.allStartPositions
                if(self.startIntersection(newPos) and self.checkinBounds(newPos) and self.checkPoints(numPoints)):#check intersection, inbounds, and points
                    #self.findandreplace(self.player1Ships[x].position,newPos)
                    self.player1Ships[x].position = newPos
                    self.points = self.points - abs(numPoints)
                    self.addtolist(newPos)
                    #print self.allStartPositions
                else:
                    self.addtolist(self.player1Ships[x].position)
                    print "There is an intersection, or ship is out of bounds, or out of points. Reenter valid information."
                    return False
                
                
            else:#player2
                while(shipName != self.player2Ships[x].name):
                    x = x + 1
                currentPos = self.player2Ships[x].position
                if(type(self.player2Ships[x]) is Patrol):#Patrol Can't change course, only one square.#################NEED TO CHECK
                    print "Patrol can't cometocourse"
                    return False
                #determining the current course
                currCourse = self.findcourse(player,shipName)

                #Determining new positions based on new course
                newPos = []#position after rotation
                if(len(self.player2Ships[x].position) == 3):#its a destroyer
                    if(course == 0 or course == 180):
                        factor = 1
                        for y in range(0,len(self.player2Ships[x].position)):
                            newPos.append([self.player2Ships[x].position[1][0],((self.player2Ships[x].position[1][1])-factor)])
                            factor = factor - 1
                    elif(course == 45 or course == 225):
                        factor = 1
                        for y in range(0,len(self.player2Ships[x].position)):
                            newPos.append([((self.player2Ships[x].position[1][0])-factor),((self.player2Ships[x].position[1][1])+factor)])
                            factor = factor - 1
                    elif(course == 90 or course == 270):
                        factor = 1
                        for y in range(0,len(self.player2Ships[x].position)):
                            newPos.append([((self.player2Ships[x].position[1][0])-factor),((self.player2Ships[x].position[1][1]))])
                            factor = factor - 1
                    else:#135 or 315
                        factor = 1
                        for y in range(0,len(self.player2Ships[x].position)):
                            newPos.append([((self.player2Ships[x].position[1][0])-factor),((self.player2Ships[x].position[1][1])-factor)])
                            factor = factor - 1
                            
                else:#its a carrier
                    if(course == 0 or course == 180):
                        factor = 2
                        for y in range(0,len(self.player2Ships[x].position)):
                            newPos.append([self.player2Ships[x].position[2][0],((self.player2Ships[x].position[2][1])-factor)])
                            factor = factor - 1
                    elif(course == 45 or course == 225):
                        factor = 2
                        for y in range(0,len(self.player2Ships[x].position)):
                            newPos.append([((self.player2Ships[x].position[2][0])-factor),((self.player2Ships[x].position[2][1])+factor)])
                            factor = factor - 1
                    elif(course == 90 or course == 270):
                        factor = 2
                        for y in range(0,len(self.player2Ships[x].position)):
                            newPos.append([((self.player2Ships[x].position[2][0])-factor),((self.player2Ships[x].position[2][1]))])
                            factor = factor - 1
                    else:#135 or 315
                        factor = 2
                        for y in range(0,len(self.player2Ships[x].position)):
                            newPos.append([((self.player2Ships[x].position[2][0])-factor),((self.player2Ships[x].position[2][1])-factor)])
                            factor = factor - 1
                
                #Find how many points it takes to turn
                if(course == 0 or course==180):
                    abscourse = 0
                elif(course == 45 or course==225):
                    abscourse = 45
                elif(course == 90 or course==270):
                    abscourse = 90
                else:
                    abscourse = 135
                numRot = abs(currCourse - abscourse)/45#number of rotations
                if(len(self.player2Ships[x].position) == 3):
                    numPoints = numRot #number of points to turn destroyer
                else:
                    numPoints = numRot * 2 #x2 points to turn carrier
                    
                self.removefromlist(self.player2Ships[x].position)#removing old values so that there will be no intersections
        
                if(self.startIntersection(newPos) and self.checkinBounds(newPos) and self.checkPoints(numPoints)):#check intersection, inbounds, and points
                    #self.findandreplace(self.player1Ships[x].position,newPos)
                    self.player2Ships[x].position = newPos
                    self.points = self.points - abs(numPoints)
                    self.addtolist(newPos)
                else:
                    self.addtolist(self.player2Ships[x].position)
                    print "There is an intersection, or ship is out of bounds, or out of points. Reenter valid information."
                    return False
        else:#rotation doesn't work or ship doesn't exist
            print "Rotation is not valid or ship does not exist. Reenter valid information."
            return False
                                
    def move(self,player,shipName,spaces,patrolx,patroly):
        #moves a ship a given number of spaces
        
        if(not self.checkShip(shipName,player)):
            return False
        x = 0
        if(player == "Player1"):
            while(shipName != self.player1Ships[x].name):
                x = x + 1
            
            ########IF PATROL##############################
            newPatrolCoord = [int(patrolx),int(patroly)]
            currentx = self.player1Ships[x].position[0][0]
            currenty = self.player1Ships[x].position[0][1]
            distancetonew = int(pow((pow(patrolx-currentx,2)+pow(patroly-currenty,2)),0.5))#distance from old to new position
            pointsPer = 1.0/self.player1Ships[x].speed#points per move
            points = distancetonew*pointsPer#points that would be used to move to new position
            
            #print self.startIntersection([newPatrolCoord])
            #print self.checkinBounds([newPatrolCoord])
            #print self.checkPoints(points)

            if((type(self.player1Ships[x]) is Patrol)):
                if(self.startIntersection([newPatrolCoord]) and self.checkinBounds([newPatrolCoord]) and self.checkPoints(points)):
                    self.points = self.points - abs(points)
                    self.removefromlist(self.player1Ships[x].position)
                    self.addtolist([newPatrolCoord])
                    self.player1Ships[x].position = [newPatrolCoord]
                    return
                else:
                    print "There is an intersection, or ship is out of bounds, or out of points. Reenter valid information."
                    return False
            #############################################

            currentPos = self.player1Ships[x].position 
            currCourse = self.findcourse(player,shipName)
            newPosition = []
            if(currCourse == 0 or currCourse == 180):
                for y in range(0,len(currentPos)):
                    newx = currentPos[y][0]
                    newy = currentPos[y][1]+spaces
                    newCoord = [newx,newy]
                    newPosition.append(newCoord)
            elif(currCourse == 90 or currCourse == 270):
                for y in range(0,len(currentPos)):
                    newx = currentPos[y][0]+spaces
                    newy = currentPos[y][1]
                    newCoord = [newx,newy]
                    newPosition.append(newCoord)
            elif(currCourse == 45 or currCourse == 225):
                for y in range(0,len(currentPos)):
                    newx = currentPos[y][0]+spaces
                    newy = currentPos[y][1]-spaces
                    newCoord = [newx,newy]
                    newPosition.append(newCoord)
            else:#currCourse == 135 or 315
                for y in range(0,len(currentPos)):
                    newx = currentPos[y][0]+spaces
                    newy = currentPos[y][1]+spaces
                    newCoord = [newx,newy]
                    newPosition.append(newCoord)
            #make all checks
            pointsPerSpace = 1.0/self.player1Ships[x].speed
            pointsUsed = pointsPerSpace*spaces
            self.removefromlist(self.player1Ships[x].position)#removing old values so that there will be no intersections
            if(self.checkPoints(pointsUsed) and self.checkinBounds(newPosition) and self.startIntersection(newPosition)):#checks
                self.points = self.points - abs(pointsUsed)
                self.player1Ships[x].position = newPosition
                self.addtolist(newPosition)#adding to allStartPositions
            else:
                self.addtolist(self.player1Ships[x].position)
                print "There is an intersection, the new position is out of bounds, or there are not enough points. Reenter valid information."
                return False
             
        else:#Player2
            while(shipName != self.player2Ships[x].name):
                x = x + 1
            ########IF PATROL##############################
            newPatrolCoord = [patrolx,patroly]
            currentx = self.player2Ships[x].position[0][0]
            currenty = self.player2Ships[x].position[0][1]
            distancetonew = int(pow((pow(patrolx-currentx,2)+pow(patroly-currenty,2)),0.5))#distance from old to new position
            pointsPer = 1.0/self.player2Ships[x].speed#points per move
            points = distancetonew*pointsPer#points that would be used to move to new position
            if((type(self.player2Ships[x]) is Patrol)):
                if(self.startIntersection([newPatrolCoord]) and self.checkinBounds([newPatrolCoord]) and self.checkPoints(points)):
                    self.points = self.points - abs(points)
                    self.removefromlist(self.player2Ships[x].position)
                    self.addtolist([newPatrolCoord])
                    self.player2Ships[x].position = [newPatrolCoord]
                    return
                else:
                    print "There is an intersection, or ship is out of bounds, or out of points. Reenter valid information."
                    return False
            #############################################
            currentPos = self.player2Ships[x].position 
            currCourse = self.findcourse(player,shipName)
            newPosition = []
            if(currCourse == 0 or currCourse == 180):
                for y in range(0,len(currentPos)):
                    newx = currentPos[y][0]
                    newy = currentPos[y][1]+spaces
                    newCoord = [newx,newy]
                    newPosition.append(newCoord)
            elif(currCourse == 90 or currCourse == 270):
                for y in range(0,len(currentPos)):
                    newx = currentPos[y][0]+spaces
                    newy = currentPos[y][1]
                    newCoord = [newx,newy]
                    newPosition.append(newCoord)
            elif(currCourse == 45 or currCourse == 225):
                for y in range(0,len(currentPos)):
                    newx = currentPos[y][0]+spaces
                    newy = currentPos[y][1]-spaces
                    newCoord = [newx,newy]
                    newPosition.append(newCoord)
            else:#currCourse == 135 or 315
                for y in range(0,len(currentPos)):
                    newx = currentPos[y][0]+spaces
                    newy = currentPos[y][1]+spaces
                    newCoord = [newx,newy]
                    newPosition.append(newCoord)
            #make all checks
            pointsPerSpace = 1.0/self.player2Ships[x].speed
            pointsUsed = pointsPerSpace*spaces
            self.removefromlist(self.player2Ships[x].position)#removing old values so that there will be no intersections

            if(self.checkPoints(pointsUsed) and self.checkinBounds(newPosition) and self.startIntersection(newPosition)):#checks
                self.points = self.points - abs(pointsUsed)
                self.player2Ships[x].position = newPosition
                self.addtolist(newPosition)#adding to allStartPositions
            else:
                self.addtolist(self.player2Ships[x].position)
                print "There is an intersection, the new position is out of bounds, or there are not enough points. Reenter valid information."
                return False

    def radarFind(self,player):
        #radarFind, runs through the enemy list and sees if any enemy ships are in range of friendly ships
        #It then prints the player field with enemy included
        if(player == "Player1"):  
            intersectionPoints = []
            for x in range(0,len(self.player1Ships)):
                if(len(self.player1Ships[x].position) == 1):#Patrol
                    centerX = self.player1Ships[x].position[0][0]
                    centerY = self.player1Ships[x].position[0][1]
                elif(len(self.player1Ships[x].position) == 3):#Destroyer
                    centerX = self.player1Ships[x].position[1][0]
                    centerY = self.player1Ships[x].position[1][1]
                else:#Carrier
                    centerX = self.player1Ships[x].position[2][0]
                    centerY = self.player1Ships[x].position[2][1]
                
                maxX = centerX + self.player1Ships[x].radar
                maxY = centerY + self.player1Ships[x].radar
                minX = centerX - self.player1Ships[x].radar
                minY = centerY - self.player1Ships[x].radar
                
                #print "maxX, maxY, minX, minY "+str(maxX)+" "+str(maxY)+" "+str(minX) +" "+ str(minY)
                shipRadarList = [] 
                for z in range(minX,maxX+1):#potential radar intersection points
                    for p in range(minY,maxY+1):
                        shipRadarList.append([z,p])
                #print shipRadarList
                for y in range(0,len(self.player1Ships[x].position)):#remove the ship points from the potential intersection list
                    shipRadarList.remove(self.player1Ships[x].position[y])
                
                for y in range(0,len(self.player2Ships)):#check to see if enemy ships intersect any of the points
                    for z in range(0,len(shipRadarList)):
                        if(shipRadarList[z] in self.player2Ships[y].position):
                            intersectionPoints.append(shipRadarList[z])
                            if(shipRadarList[z] not in self.player1History):
                                self.player1History.append(shipRadarList[z])
                #print intersectionPoints
            #Will print the field of the player
            for x in range(0,1):#print extra spaces
                print " "
            field =[[0 for j in range(self.sizeFieldx)] for i in range(self.sizeFieldy)]
            for y in range (0,self.sizeFieldy):
                for x in range (0,self.sizeFieldx):
                    field[y][x] = x
                    
            carrierSym = '\033[94m'
            destroyerSym ='\033[94m'
            patrolSym = '\033[94m'
            endSym = '\033[0m'
            for x in range(0,len(self.player1Ships)):
                if(len(self.player1Ships[x].position) != 0):
                    for y in range(0,len(self.player1Ships[x].position)):
                        if(type(self.player1Ships[x]) is Carrier):
                            symbol = carrierSym
                        elif(type(self.player1Ships[x]) is Destroyer):
                            symbol = destroyerSym
                        else:
                            symbol = patrolSym
                        #print self.allStartPositions
                        field[self.player1Ships[x].position[y][1]][self.player1Ships[x].position[y][0]] = symbol+self.player1Ships[x].name+endSym
            
            for x in range(0,len(intersectionPoints)):#Check enemy ships
                field[intersectionPoints[x][1]][intersectionPoints[x][0]] = "\033[5;41;32mEE\033[0m" + endSym
                
        
                            
        else:#Player2  
            intersectionPoints = []
            for x in range(0,len(self.player2Ships)):
                if(len(self.player2Ships[x].position) == 1):#Patrol
                    centerX = self.player2Ships[x].position[0][0]
                    centerY = self.player2Ships[x].position[0][1]
                elif(len(self.player2Ships[x].position) == 3):#Destroyer
                    centerX = self.player2Ships[x].position[1][0]
                    centerY = self.player2Ships[x].position[1][1]
                else:#Carrier
                    centerX = self.player2Ships[x].position[2][0]
                    centerY = self.player2Ships[x].position[2][1]
                
                maxX = centerX + self.player2Ships[x].radar
                maxY = centerY + self.player2Ships[x].radar
                minX = centerX - self.player2Ships[x].radar
                minY = centerY - self.player2Ships[x].radar
                
                shipRadarList = [] 
                for z in range(minX,maxX+1):#potential radar intersection points
                    for p in range(minY,maxY+1):
                        shipRadarList.append([z,p])
                for y in range(0,len(self.player2Ships[x].position)):#remove the ship points from the potential intersection list
                    shipRadarList.remove(self.player2Ships[x].position[y])

                for y in range(0,len(self.player1Ships)):#check to see if enemy ships intersect any of the points
                    for z in range(0,len(shipRadarList)):
                        if(shipRadarList[z] in self.player1Ships[y].position):
                            intersectionPoints.append(shipRadarList[z])
                            if(shipRadarList[z] not in self.player2History):
                                self.player2History.append(shipRadarList[z])
        
            #Will print the field of the player
            for x in range(0,1):#print extra spaces
                print " "
            field =[[0 for j in range(self.sizeFieldx)] for i in range(self.sizeFieldy)]
            for y in range (0,self.sizeFieldy):
                for x in range (0,self.sizeFieldx):
                    field[y][x] = x
                    
            carrierSym = '\033[94m'
            destroyerSym ='\033[94m'
            patrolSym = '\033[94m'
            endSym = '\033[0m'
            for x in range(0,len(self.player2Ships)):
                if(len(self.player2Ships[x].position) != 0):
                    for y in range(0,len(self.player2Ships[x].position)):
                        if(type(self.player2Ships[x]) is Carrier):
                            symbol = carrierSym
                        elif(type(self.player2Ships[x]) is Destroyer):
                            symbol = destroyerSym
                        else:
                            symbol = patrolSym
                        #print self.allStartPositions
                        field[self.player2Ships[x].position[y][1]][self.player2Ships[x].position[y][0]] = symbol+self.player2Ships[x].name+endSym
            
            for x in range(0,len(intersectionPoints)):#Check enemy ships
                field[intersectionPoints[x][1]][intersectionPoints[x][0]] = "\033[5;41;32mEE\033[0m" + endSym

        #####################################################
        #print intersectionPoints
        #This prints for both Player1 and Player2
        yAxisPlaceHolders = [0 for i in range(self.sizeFieldy)]
        for y in range(0,self.sizeFieldy):
            yAxisPlaceHolders[y] = y
        for y in range (0,self.sizeFieldy):
            if(y<10):
                print str(yAxisPlaceHolders[y])+"||",
            else:
                print str(yAxisPlaceHolders[y])+"|",
            for x in range(0,self.sizeFieldx):
                if(x < self.sizeFieldx-1 and not isinstance(field[y][x],basestring)):
                    if(x<10):
                        print str(field[y][x])+"|",
                    else:
                        print str(field[y][x]),
                elif(x < self.sizeFieldx-1 and isinstance(field[y][x],basestring)):
                    print str(field[y][x]),
                else:
                    print str(field[y][x])
    
                    
    def allShipsRadar(self,player):
        #allShipsRadar, runs through the enemy list and sees if any enemy ships are in range of friendly ships
        #It also shows the radar of each ship in a different color on the map.
        #It then prints the player field with radar and enemy included
        if(player == "Player1"):  
            intersectionPoints = []
            allShipsRadarList = []
            for x in range(0,len(self.player1Ships)):
                if(len(self.player1Ships[x].position) == 1):#Patrol
                    centerX = self.player1Ships[x].position[0][0]
                    centerY = self.player1Ships[x].position[0][1]
                elif(len(self.player1Ships[x].position) == 3):#Destroyer
                    centerX = self.player1Ships[x].position[1][0]
                    centerY = self.player1Ships[x].position[1][1]
                else:#Carrier
                    centerX = self.player1Ships[x].position[2][0]
                    centerY = self.player1Ships[x].position[2][1]
                
                maxX = centerX + self.player1Ships[x].radar
                maxY = centerY + self.player1Ships[x].radar
                minX = centerX - self.player1Ships[x].radar
                minY = centerY - self.player1Ships[x].radar
                
                #print "maxX, maxY, minX, minY "+str(maxX)+" "+str(maxY)+" "+str(minX) +" "+ str(minY)
                shipRadarList = [] 
                for z in range(minX,maxX+1):#potential radar intersection points
                    for p in range(minY,maxY+1):
                        shipRadarList.append([z,p])
                #print shipRadarList
                for y in range(0,len(self.player1Ships[x].position)):#remove the ship points from the potential intersection list
                    shipRadarList.remove(self.player1Ships[x].position[y])
                
                for y in range(0,len(self.player2Ships)):#check to see if enemy ships intersect any of the points
                    for z in range(0,len(shipRadarList)):
                        if(shipRadarList[z] in self.player2Ships[y].position):
                            intersectionPoints.append(shipRadarList[z])
                            #shipRadarList.remove(shipRadarList[z])
                            if(shipRadarList[z] not in self.player1History):
                                self.player1History.append(shipRadarList[z])

                for r in range(0,len(shipRadarList)):
                    if(shipRadarList[r] not in allShipsRadarList):
                        allShipsRadarList.append(shipRadarList[r])

            for x in range(0,len(intersectionPoints)):
                if(intersectionPoints[x] in allShipsRadarList):
                    allShipsRadarList.remove(intersectionPoints[x])
                    
                #print intersectionPoints
            #Will print the field of the player
            for x in range(0,1):#print extra spaces
                print " "
            field =[[0 for j in range(self.sizeFieldx)] for i in range(self.sizeFieldy)]
            for y in range (0,self.sizeFieldy):
                for x in range (0,self.sizeFieldx):
                    field[y][x] = x
                    
            carrierSym = '\033[94m'
            destroyerSym ='\033[94m'
            patrolSym = '\033[94m'
            endSym = '\033[0m'

            radarSym = '\033[97m'

            for x in range(0,len(self.player1Ships)):
                if(len(self.player1Ships[x].position) != 0):
                    for y in range(0,len(self.player1Ships[x].position)):
                        if(type(self.player1Ships[x]) is Carrier):
                            symbol = carrierSym
                        elif(type(self.player1Ships[x]) is Destroyer):
                            symbol = destroyerSym
                        else:
                            symbol = patrolSym
                        #print self.allStartPositions
                        field[self.player1Ships[x].position[y][1]][self.player1Ships[x].position[y][0]] = symbol+self.player1Ships[x].name+endSym
            
            for x in range(0,len(intersectionPoints)):#Check enemy ships
                field[intersectionPoints[x][1]][intersectionPoints[x][0]] = "\033[5;41;32mEE\033[0m" + endSym
            #for x in range(0,len(shipRadarList)):
                #field[shipRadarList[x][1]][shipRadarList[x][0]] = radarSym + str(shipRadarList[x][0]) + endSym
                
        
                            
        else:#Player2  
            intersectionPoints = []
            allShipsRadarList = []
            for x in range(0,len(self.player2Ships)):
                if(len(self.player2Ships[x].position) == 1):#Patrol
                    centerX = self.player2Ships[x].position[0][0]
                    centerY = self.player2Ships[x].position[0][1]
                elif(len(self.player2Ships[x].position) == 3):#Destroyer
                    centerX = self.player2Ships[x].position[1][0]
                    centerY = self.player2Ships[x].position[1][1]
                else:#Carrier
                    centerX = self.player2Ships[x].position[2][0]
                    centerY = self.player2Ships[x].position[2][1]
                
                maxX = centerX + self.player2Ships[x].radar
                maxY = centerY + self.player2Ships[x].radar
                minX = centerX - self.player2Ships[x].radar
                minY = centerY - self.player2Ships[x].radar
                
                shipRadarList = [] 
                for z in range(minX,maxX+1):#potential radar intersection points
                    for p in range(minY,maxY+1):
                        shipRadarList.append([z,p])
                for y in range(0,len(self.player2Ships[x].position)):#remove the ship points from the potential intersection list
                    shipRadarList.remove(self.player2Ships[x].position[y])

                for y in range(0,len(self.player1Ships)):#check to see if enemy ships intersect any of the points
                    for z in range(0,len(shipRadarList)):
                        if(shipRadarList[z] in self.player1Ships[y].position):
                            intersectionPoints.append(shipRadarList[z])
                            #shipRadarList.remove(shipRadarList[z])
                            if(shipRadarList[z] not in self.player2History):
                                self.player2History.append(shipRadarList[z])

                for r in range(0,len(shipRadarList)):
                    if(shipRadarList[r] not in allShipsRadarList):
                        allShipsRadarList.append(shipRadarList[r])
                        
            for x in range(0,len(intersectionPoints)):
                if(intersectionPoints[x] in allShipsRadarList):
                    allShipsRadarList.remove(intersectionPoints[x])
                    
            #Will print the field of the player
            for x in range(0,1):#print extra spaces
                print " "

            field =[[0 for j in range(self.sizeFieldx)] for i in range(self.sizeFieldy)]
            for y in range (0,self.sizeFieldy):
                for x in range (0,self.sizeFieldx):
                    field[y][x] = x
                    
            carrierSym = '\033[94m'
            destroyerSym ='\033[94m'
            patrolSym = '\033[94m'
            endSym = '\033[0m'

            radarSym = '\033[97m'

            for x in range(0,len(self.player2Ships)):
                if(len(self.player2Ships[x].position) != 0):
                    for y in range(0,len(self.player2Ships[x].position)):
                        if(type(self.player2Ships[x]) is Carrier):
                            symbol = carrierSym
                        elif(type(self.player2Ships[x]) is Destroyer):
                            symbol = destroyerSym
                        else:
                            symbol = patrolSym
                        #print self.allStartPositions
                        field[self.player2Ships[x].position[y][1]][self.player2Ships[x].position[y][0]] = symbol+self.player2Ships[x].name+endSym
            
            for x in range(0,len(intersectionPoints)):#Check enemy ships
                field[intersectionPoints[x][1]][intersectionPoints[x][0]] = "\033[5;41;32mEE\033[0m" + endSym
            #for x in range(0,len(shipRadarList)):#ships radar
                #field[shipRadarList[x][1]][shipRadarList[x][0]] = radarSym + str(shipRadarList[x][0]) + endSym

        #####################################################
        #print intersectionPoints
        #This prints for both Player1 and Player2
        yAxisPlaceHolders = [0 for i in range(self.sizeFieldy)]
        for y in range(0,self.sizeFieldy):
            yAxisPlaceHolders[y] = y
        for y in range (0,self.sizeFieldy):
            if(y<10):
                print str(yAxisPlaceHolders[y])+"||",
            else:
                print str(yAxisPlaceHolders[y])+"|",
            for x in range(0,self.sizeFieldx):
                if(x < self.sizeFieldx-1 and (not isinstance(field[y][x],basestring)) and ([x,y] not in allShipsRadarList)):#regular numbers
                    if(x<10):
                        print str(field[y][x])+"|",
                    else:
                        print str(field[y][x]),
                elif(x < self.sizeFieldx-1 and (not isinstance(field[y][x],basestring)) and ([x,y] in allShipsRadarList)):#radar
                    if(x<10):
                        print radarSym + str(field[y][x])+"|" + endSym,
                    else:
                        print radarSym + str(field[y][x]) + endSym,
                elif(x < self.sizeFieldx-1 and isinstance(field[y][x],basestring)):
                    print str(field[y][x]),
                else:
                    print str(field[y][x])
    
                    
    def beforeFireMap(self,player,lightFriendShip,enemyX,enemyY):
        #beforeFireMap prints the map of the fireing ship(lighFriendShip) in blinking green and the target in blinking red. similar to radarFind.
        
        if(player == "Player1"):  
            intersectionPoints = []
            for x in range(0,len(self.player1Ships)):
                if(len(self.player1Ships[x].position) == 1):#Patrol
                    centerX = self.player1Ships[x].position[0][0]
                    centerY = self.player1Ships[x].position[0][1]
                elif(len(self.player1Ships[x].position) == 3):#Destroyer
                    centerX = self.player1Ships[x].position[1][0]
                    centerY = self.player1Ships[x].position[1][1]
                else:#Carrier
                    centerX = self.player1Ships[x].position[2][0]
                    centerY = self.player1Ships[x].position[2][1]
                
                maxX = centerX + self.player1Ships[x].radar
                maxY = centerY + self.player1Ships[x].radar
                minX = centerX - self.player1Ships[x].radar
                minY = centerY - self.player1Ships[x].radar
                
                #print "maxX, maxY, minX, minY "+str(maxX)+" "+str(maxY)+" "+str(minX) +" "+ str(minY)
                shipRadarList = [] 
                for z in range(minX,maxX+1):#potential radar intersection points
                    for p in range(minY,maxY+1):
                        shipRadarList.append([z,p])
                #print shipRadarList
                for y in range(0,len(self.player1Ships[x].position)):#remove the ship points from the potential intersection list
                    shipRadarList.remove(self.player1Ships[x].position[y])
                
                for y in range(0,len(self.player2Ships)):#check to see if enemy ships intersect any of the points
                    for z in range(0,len(shipRadarList)):
                        if(shipRadarList[z] in self.player2Ships[y].position):
                            intersectionPoints.append(shipRadarList[z])
                            if(shipRadarList[z] not in self.player1History):
                                self.player1History.append(shipRadarList[z])
                #print intersectionPoints
            #Will print the field of the player
            for x in range(0,1):#print extra spaces
                print " "
            field =[[0 for j in range(self.sizeFieldx)] for i in range(self.sizeFieldy)]
            for y in range (0,self.sizeFieldy):
                for x in range (0,self.sizeFieldx):
                    field[y][x] = x
                    
            carrierSym = '\033[94m'
            destroyerSym ='\033[94m'
            patrolSym = '\033[94m'
            endSym = '\033[0m'
            for x in range(0,len(self.player1Ships)):
                if(len(self.player1Ships[x].position) != 0):
                    for y in range(0,len(self.player1Ships[x].position)):
                        if(type(self.player1Ships[x]) is Carrier):
                            symbol = carrierSym
                        elif(type(self.player1Ships[x]) is Destroyer):
                            symbol = destroyerSym
                        else:
                            symbol = patrolSym
                        #print self.allStartPositions
                        field[self.player1Ships[x].position[y][1]][self.player1Ships[x].position[y][0]] = symbol+self.player1Ships[x].name+endSym
            
            for x in range(0,len(intersectionPoints)):#Check enemy ships
                field[intersectionPoints[x][1]][intersectionPoints[x][0]] = "\033[1;41;32mEE\033[0m" + endSym

            friendShip = 1000#just initilizing, will never get to 1000
            for x in range(0,len(self.player1Ships)):
                if(self.player1Ships[x].name == lightFriendShip):
                    friendShip = x
                    break
            if(friendShip == 1000):
                print "Error in Friendly Ship. Retry."
                return False
            
            for x in range(0,len(self.player1Ships[friendShip].position)):#Friend Ship--firing ship--blink green
                field[self.player1Ships[friendShip].position[x][1]][self.player1Ships[friendShip].position[x][0]] = "\033[5;42;34mFF\033[0m"
            
            field[enemyY][enemyX] = "\033[5;41;37mEE\033[0m"
            
                                            
        else:#Player2  
            intersectionPoints = []
            for x in range(0,len(self.player2Ships)):
                if(len(self.player2Ships[x].position) == 1):#Patrol
                    centerX = self.player2Ships[x].position[0][0]
                    centerY = self.player2Ships[x].position[0][1]
                elif(len(self.player2Ships[x].position) == 3):#Destroyer
                    centerX = self.player2Ships[x].position[1][0]
                    centerY = self.player2Ships[x].position[1][1]
                else:#Carrier
                    centerX = self.player2Ships[x].position[2][0]
                    centerY = self.player2Ships[x].position[2][1]
                
                maxX = centerX + self.player1Ships[x].radar
                maxY = centerY + self.player1Ships[x].radar
                minX = centerX - self.player1Ships[x].radar
                minY = centerY - self.player1Ships[x].radar
                
                shipRadarList = [] 
                for z in range(minX,maxX+1):#potential radar intersection points
                    for p in range(minY,maxY+1):
                        shipRadarList.append([z,p])
                for y in range(0,len(self.player2Ships[x].position)):#remove the ship points from the potential intersection list
                    shipRadarList.remove(self.player2Ships[x].position[y])

                for y in range(0,len(self.player1Ships)):#check to see if enemy ships intersect any of the points
                    for z in range(0,len(shipRadarList)):
                        if(shipRadarList[z] in self.player1Ships[y].position):
                            intersectionPoints.append(shipRadarList[z])
                            if(shipRadarList[z] not in self.player2History):
                                self.player2History.append(shipRadarList[z])
        
            #Will print the field of the player
            for x in range(0,1):#print extra spaces
                print " "
            field =[[0 for j in range(self.sizeFieldx)] for i in range(self.sizeFieldy)]
            for y in range (0,self.sizeFieldy):
                for x in range (0,self.sizeFieldx):
                    field[y][x] = x
                    
            carrierSym = '\033[94m'
            destroyerSym ='\033[94m'
            patrolSym = '\033[94m'
            endSym = '\033[0m'
            for x in range(0,len(self.player2Ships)):
                if(len(self.player2Ships[x].position) != 0):
                    for y in range(0,len(self.player2Ships[x].position)):
                        if(type(self.player2Ships[x]) is Carrier):
                            symbol = carrierSym
                        elif(type(self.player2Ships[x]) is Destroyer):
                            symbol = destroyerSym
                        else:
                            symbol = patrolSym
                        #print self.allStartPositions
                        field[self.player2Ships[x].position[y][1]][self.player2Ships[x].position[y][0]] = symbol+self.player2Ships[x].name+endSym
            
            for x in range(0,len(intersectionPoints)):#Check enemy ships
                field[intersectionPoints[x][1]][intersectionPoints[x][0]] = "\033[1;41;32mEE\033[0m" + endSym

            friendShip = 1000#just initilizing, will never get to 1000
            for x in range(0,len(self.player2Ships)):
                if(self.player2Ships[x].name == lightFriendShip):
                    friendShip = x
                    break
            if(friendShip == 1000):
                print "Error in Friendly Ship. Retry."
                return False
            
            for x in range(0,len(self.player2Ships[friendShip].position)):#Friend Ship--firing ship--blink green
                field[self.player2Ships[friendShip].position[x][1]][self.player2Ships[friendShip].position[x][0]] = "\033[5;42;34mFF\033[0m"
            
            field[enemyY][enemyX] = "\033[5;41;37mEE\033[0m"

        #print intersectionPoints
        #This prints for both Player1 and Player2
        yAxisPlaceHolders = [0 for i in range(self.sizeFieldy)]
        for y in range(0,self.sizeFieldy):
            yAxisPlaceHolders[y] = y
        for y in range (0,self.sizeFieldy):
            if(y<10):
                print str(yAxisPlaceHolders[y])+"||",
            else:
                print str(yAxisPlaceHolders[y])+"|",
            for x in range(0,self.sizeFieldx):
                if(x < self.sizeFieldx-1 and not isinstance(field[y][x],basestring)):
                    if(x<10):
                        print str(field[y][x])+"|",
                    else:
                        print str(field[y][x]),
                elif(x < self.sizeFieldx-1 and isinstance(field[y][x],basestring)):
                    print str(field[y][x]),
                else:
                    print str(field[y][x])
    
    def removeDeadShip(self):
        #removes ship with 0 health
        
        count = 0
        while(count <= len(self.player1Ships)-1):
            if(self.player1Ships[count].health <= 0):
                for y in range(0,len(self.player1Ships[count].position)):
                    self.allStartPositions.remove(self.player1Ships[count].position[y])
                self.player1DeadShips.append(self.player1Ships[count])
                self.player1Ships.remove(self.player1Ships[count])
            else:
                count = count + 1
                
        #print len(self.player2Ships)
        #print self.player2Ships
        count = 0
        while(count <= len(self.player2Ships)-1):
            if(self.player2Ships[count].health <= 0):
                for y in range(0,len(self.player2Ships[count].position)):
                    self.allStartPositions.remove(self.player2Ships[count].position[y])
                self.player2DeadShips.append(self.player2Ships[count])
                self.player2Ships.remove(self.player2Ships[count])
            else:
                count = count + 1
        
                            
    def weaponsPackage(self,player,shipName,weapon,targetX,targetY):
        #Fire weapon at specified target location
        #shipName is ship that weapon is being fire from
        
        if(player == "Player1"):
            if(not self.checkShip(shipName,player)):
                print "Ship does not exist. Reenter valid information."
                return False

            if(weapon =="ASM" or weapon =="HARM" or weapon =="SRM" or weapon =="Planes"):
                #Do nothing
                unusedVariable = 0
            else:
                print "Weapon does not exist. Reenter valid information."
                return False
            if(not self.checkinBounds([[targetX,targetY]])):
                print "Target is either out of bounds or not an int. Reenter valid information."
                return False
            ##################
            count = 0#counter
            for x in range(0,len(self.player1Ships)):#Find Ship that is firing
                if(self.player1Ships[x].name == shipName):
                    count = x
            if(type(self.player1Ships[count]) is Patrol):#Check if Patrol
                print "Patrol cannot engage enemy. Reenter valid information."
                return False
            if(len(self.player1Ships[count].position) == 3):
                middle = 1#middle of the boat
            else:#carrier length == 5
                middle = 2
            distancetoTarget = int(pow(pow((self.player1Ships[count].position[middle][0] - targetX),2) + pow((self.player1Ships[count].position[middle][1] - targetY),2),0.5))
            ####################
            if(weapon == "ASM" and distancetoTarget > self.ASMrange):
                print "Weapon out of range."
                return False
            if(weapon == "HARM" and distancetoTarget > self.HARMrange):
                print "Weapon out of range."
                return False
            if(weapon == "SRM" and distancetoTarget > self.SRMrange):
                print "Weapon out of range."
                return False
            if(weapon == "Planes" and distancetoTarget > self.Planesrange):
                print "Weapon out of range."
                return False
            #####################
            #print type(self.player1Ships[count]) is not Destroyer
            if((weapon == "ASM" or weapon == "SRM" or weapon == "HARM") and (type(self.player1Ships[count]) is not Destroyer)):#wrong weapon for ship
                print "Ship does not carry this weapon. Reenter valid information."
                return False
            if(weapon == "Planes" and type(self.player1Ships[count]) is not Carrier):
                print "Ship does not carry this weapon. Reenter valid information."
                return False
            #####################
            if(weapon == "ASM"):
                points = self.ASMpoints
            elif(weapon == "SRM"):
                points = self.SRMpoints
            elif(weapon == "Planes"):
                points = self.Planespoints
            else:#for HARM Missle
                points = self.HARMpoints
            
            if(self.checkPoints(points)):
                if(weapon == "ASM"):
                    
                    self.beforeFireMap(player,shipName,targetX,targetY)
                    print " "
                    while(True):#ask user if he wants to retaliate
                        mapCode = raw_input("\033[1;41;37mDo you wish to engage? You will have one more chance to cancel. (yes/no):\033[0m" + " ")
                        print " "
                        if(mapCode == "yes"):
                            print "   "+"\033[1;41;37m---Proceed to Weapon Summary---\033[0m"
                            print "           ."
                            print "           ."
                            print "           ."
                            print "           ."
                            print "           ."
                            #time.sleep(1)
                            break
                        elif(mapCode == "no"):
                            print "ASM Missle Battery is Standing Down."
                            return False
                        else:
                            print "Reenter valid information."
            
                    
                    
                    #print "   "+"\033[1;47;30m------------------------------\033[0m"
                    print "   "+"\033[1;47;31m  ASM Weapon Package Summary  \033[0m"
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mShip Name of Origin:          \033[0m" +" "+shipName
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mTarget Position:              \033[0m"+" "+ str([targetX,targetY])
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mDistance to Target            \033[0m"+" "+str(distancetoTarget)
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mPoints left after Launch:     \033[0m"+" "+str(self.points - points)
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mMissle Flight Time:           \033[0m"+" "+str(int(distancetoTarget/6))
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mASM Missles Left after Launch:\033[0m"+" "+str(self.player1Ships[count].ASM - 1)
                    print "   "+"\033[1;47;30m------------------------------\033[0m"
                    print " "
                    while(True):#ask user if he wants to retaliate
                        launchCode = raw_input("\033[5;41;37mDo you wish to proceed with ASM Missle Launch? (yes/no):\033[0m" + " ")
                        print " "
                        if(launchCode == "yes"):
                            print "   "+"\033[1;41;37m---Entering Snap Count---\033[0m"
                            print "           ."
                            time.sleep(1)
                            print "   "+"\033[1;41;37m---Missle Armed---\033[0m"
                            print "           ."
                            time.sleep(1)
                            print "   "+"\033[1;41;37m---MISSLE AWAY---\033[0m"
                            for h in range(0,int(distancetoTarget/6)):
                                print "           ."
                                time.sleep(1)
                            break
                        elif(launchCode == "no"):
                            print "ASM Missle Battery is Standing Down."
                            return False
                        else:
                            print "Reenter valid information."
            
                    
                    self.ASMflag = 1#for HARM
                    if(self.player1Ships[count].position[1] not in self.ASMposition):#place position the ASM was fired from in list
                        self.ASMposition.append(self.player1Ships[count].position[1])
                    self.points = self.points - points#take points
                    self.player1Ships[count].ASM = self.player1Ships[count].ASM - 1#loses a missle
                    if(distancetoTarget<=10):
                        hit = 1 #100% change of hitting
                    else:
                        percentage = int(30 + (80*(50-distancetoTarget)/50))#chance of hitting if over 10 distance
                    
                        percentList = []
                        for y in range(0,percentage):
                            percentList.append(1)
                        for y in range(percentage, 100):
                            percentList.append(0)
                        randNum = random.randrange(0,99,1)#random number generator between 0 and 99 and increasing by 1
                        #print len(percentList)
                        #print percentList
                        #print randNum
                        if(percentList[randNum] == 1):
                            hit = 1
                        else:
                            hit = 0
                            #time.sleep(2)#wait 2 seconds
                            print "          "+"\033[1;44;37mMiss\033[0m"#print miss
                            print " "
                            self.removeDeadShip()
                            return
                    if(hit == 1):
                        for y in range(0,len(self.player2Ships)):
                            if([targetX,targetY] in self.player2Ships[y].position):
                                self.player2Ships[y].health = self.player2Ships[y].health-self.ASMfixedDamage-random.randrange(0,self.ASMvariableDamage,1)#20(fixed)+20(rand)
                                #time.sleep(2)#wait 2 seconds
                                print "          "+"\033[1;41;37mHit\033[0m"#print hit
                                print " "
                                self.removeDeadShip()
                                return
                        #time.sleep(2)#wait 2 seconds
                        print "          "+"\033[1;44;37mMiss\033[0m"#print miss
                        print " "
                        self.removeDeadShip()
                        return

                elif(weapon == "HARM"):
                    
                    self.points = self.points - points
                    self.player1Ships[count].HARM = self.player1Ships[count].HARM - 1#loses a missle
                    self.ASMflag = 0
                    self.ASMposition = []
                    for y in range(0,len(self.player2Ships)):
                        if([targetX,targetY] in self.player2Ships[y].position):
                            self.player2Ships[y].health = self.player2Ships[y].health-self.HARMfixedDamage-random.randrange(0,self.HARMvariableDamage,1)#20(fixed)+10(rand)
                            print "   "+"\033[1;41;37mMISSLE AWAY\033[0m"
                            for e in range(0,2):
                                time.sleep(1)#wait 2 seconds
                                print "        ."
                            print "       "+"\033[1;41;37mHit\033[0m"#print hit
                            print " "
                            self.removeDeadShip()
                            return
                    print "   "+"\033[1;41;37mMISSLE AWAY\033[0m"
                    for e in range(0,2):
                        time.sleep(1)#wait 2 seconds
                        print "        ."
                    print "       "+"\033[1;44;37mMiss\033[0m"#print miss
                    print " "
                    self.removeDeadShip()
                    return
                
                elif(weapon == "SRM"):
                    
                    self.beforeFireMap(player,shipName,targetX,targetY)
                    print " "
                    while(True):#ask user if he wants to retaliate
                        mapCode = raw_input("\033[1;41;37mDo you wish to engage? You will have one more chance to cancel. (yes/no):\033[0m" + " ")
                        print " "
                        if(mapCode == "yes"):
                            print "   "+"\033[1;41;37m---Proceed to Weapon Summary---\033[0m"
                            print "           ."
                            print "           ."
                            print "           ."
                            print "           ."
                            print "           ."
                            #time.sleep(1)
                            break
                        elif(mapCode == "no"):
                            print "SRM Missle Battery is Standing Down."
                            return False
                        else:
                            print "Reenter valid information."
            

                    print "   "+"\033[1;47;31m  SRM Weapon Package Summary  \033[0m"
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mShip Name of Origin:          \033[0m" +" "+shipName
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mTarget Position:              \033[0m"+" "+ str([targetX,targetY])
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mDistance to Target            \033[0m"+" "+str(distancetoTarget)
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mPoints left after Launch:     \033[0m"+" "+str(self.points - points)
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mMissle Flight Time:           \033[0m"+" "+str(int(distancetoTarget/6))
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mASM Missles Left after Launch:\033[0m"+" "+str(self.player1Ships[count].SRM - 1)
                    print "   "+"\033[1;47;30m------------------------------\033[0m"
                    print " "
                    while(True):#ask user if he wants to retaliate
                        launchCode = raw_input("\033[5;41;37mDo you wish to proceed with SRM Missle Launch? (yes/no):\033[0m" + " ")
                        print " "
                        if(launchCode == "yes"):
                            time.sleep(1)
                            print "   "+"\033[1;41;37m---MISSLE AWAY---\033[0m"
                            for h in range(0,1):
                                print "           ."
                                time.sleep(1)
                            break
                        elif(launchCode == "no"):
                            print "SRM Missle Battery is Standing Down."
                            return False
                        else:
                            print "Reenter valid information."
            
                    
                    self.points = self.points - points
                    self.player1Ships[count].SRM = self.player1Ships[count].SRM - 1#loses a missle
                    for y in range(0,len(self.player2Ships)):
                        if([targetX,targetY] in self.player2Ships[y].position):
                            self.player2Ships[y].health = self.player2Ships[y].health-self.SRMfixedDamage-random.randrange(0,self.SRMvariableDamage,1)#10(fixed)+10(rand)
                            #time.sleep(2)#wait 2 seconds
                            print "          "+"\033[1;41;37mHit\033[0m"#print hit
                            print " "
                            self.removeDeadShip()
                            return
                    #time.sleep(2)#wait 2 seconds
                    print "          "+"\033[1;44;37mMiss\033[0m"#print miss
                    print " "
                    self.removeDeadShip()
                    return
                
                else:#Planes -- limitless ammo

                    self.beforeFireMap(player,shipName,targetX,targetY)
                    print " "
                    while(True):#ask user if he wants to retaliate
                        mapCode = raw_input("\033[1;41;37mDo you wish to engage? You will have one more chance to cancel. (yes/no):\033[0m" + " ")
                        print " "
                        if(mapCode == "yes"):
                            print "   "+"\033[1;41;37m---Proceed to Weapon Summary---\033[0m"
                            print "           ."
                            print "           ."
                            print "           ."
                            print "           ."
                            print "           ."
                            #time.sleep(1)
                            break
                        elif(mapCode == "no"):
                            print "All Planes are Standing Down."
                            return False
                        else:
                            print "Reenter valid information."
            

                    print "   "+"\033[1;47;31m    Planes Weapon Summary     \033[0m"
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mShip Name of Origin:          \033[0m" +" "+shipName
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mTarget Position:              \033[0m"+" "+ str([targetX,targetY])
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mDistance to Target            \033[0m"+" "+str(distancetoTarget)
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mPoints left after Launch:     \033[0m"+" "+str(self.points - points)
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mMissle Flight Time:           \033[0m"+" "+str(int(distancetoTarget/6))
                    print "   "+"\033[1;47;30m------------------------------\033[0m"
                    print " "
                    while(True):#ask user if he wants to retaliate
                        launchCode = raw_input("\033[5;41;37mDo you wish to deploy your fighters? (yes/no):\033[0m" + " ")
                        print " "
                        if(launchCode == "yes"):
                            time.sleep(1)
                            print "   "+"\033[1;41;37m---PLANES AWAY---\033[0m"
                            for h in range(0,1):
                                print "           ."
                                time.sleep(1)
                            break
                        elif(launchCode == "no"):
                            print "All Planes are Standing Down."
                            return False
                        else:
                            print "Reenter valid information."
            
                    self.points = self.points - points
                    for y in range(0,len(self.player2Ships)):
                        if([targetX,targetY] in self.player2Ships[y].position):
                            self.player2Ships[y].health = self.player2Ships[y].health-self.PlanesfixedDamage-random.randrange(0,self.PlanesvariableDamage,1)#10(fixed)+20(rand)
                            #time.sleep(2)#wait 2 seconds
                            print "          "+"\033[1;41;37mHit\033[0m" #print hit
                            print " "
                            self.removeDeadShip()
                            return
                    #time.sleep(2)#wait 2 seconds
                    print "          "+"\033[1;44;37mMiss\033[0m"#print miss
                    print " "
                    self.removeDeadShip()
                    return
            
            else:#not enough points
                print "Not enough points to engage."
                print " "
                return False

        else:#Player2
            if(not self.checkShip(shipName,player)):
                print "Ship does not exist. Reenter valid information."
                return False
            if(weapon =="ASM" or weapon =="HARM" or weapon =="SRM" or weapon =="Planes"):
                #Do nothing
                unusedVariable = 0
            else:
                print "Weapon does not exist. Reenter valid information."
                return False
            if(not self.checkinBounds([[targetX,targetY]])):
                print "Target is either out of bounds or not an int. Reenter valid information."
                return False
            ##################
            count = 0#counter
            for x in range(0,len(self.player2Ships)):#Find Ship that is firing
                if(self.player2Ships[x].name == shipName):
                    count = x
            if(type(self.player2Ships[count]) is Patrol):#Check if Patrol
                print "Patrol cannot engage enemy. Reenter valid information."
                return False
            if(len(self.player2Ships[count].position) == 3):
                middle = 1#middle of the boat
            else:#carrier length == 5
                middle = 2
            distancetoTarget = int(pow(pow((self.player2Ships[count].position[middle][0] - targetX),2) + pow((self.player2Ships[count].position[middle][1] - targetY),2),0.5))
            ####################
            if(weapon == "ASM" and distancetoTarget > self.ASMrange):
                print "Weapon out of range."
                return False
            if(weapon == "HARM" and distancetoTarget > self.HARMrange):
                print "Weapon out of range."
                return False
            if(weapon == "SRM" and distancetoTarget > self.SRMrange):
                print "Weapon out of range."
                return False
            if(weapon == "Planes" and distancetoTarget > self.Planesrange):
                print "Weapon out of range."
                return False
            #####################
            if((weapon == "ASM" or weapon == "SRM" or weapon == "HARM") and (type(self.player2Ships[count]) is not Destroyer)):#wrong weapon for ship
                print "Ship does not carry this weapon. Reenter valid information."
                return False
            if(weapon == "Planes" and type(self.player2Ships[count]) is not Carrier):
                print "Ship does not carry this weapon. Reenter valid information."
                return False
            #####################
            if(weapon == "ASM"):
                points = self.ASMpoints
            elif(weapon == "SRM"):
                points = self.SRMpoints
            elif(weapon == "Planes"):
                points = self.Planespoints
            else:#for HARM Missle
                points = self.HARMpoints
            
            if(self.checkPoints(points)):
                if(weapon == "ASM"):
                    
                    self.beforeFireMap(player,shipName,targetX,targetY)
                    print " "
                    while(True):#ask user if he wants to retaliate
                        mapCode = raw_input("\033[1;41;37mDo you wish to engage? You will have one more chance to cancel. (yes/no):\033[0m" + " ")
                        print " "
                        if(mapCode == "yes"):
                            print "   "+"\033[1;41;37m---Proceed to Weapon Summary---\033[0m"
                            print "           ."
                            print "           ."
                            print "           ."
                            print "           ."
                            print "           ."
                            #time.sleep(1)
                            break
                        elif(mapCode == "no"):
                            print "ASM Missle Battery is Standing Down."
                            return False
                        else:
                            print "Reenter valid information."
            

                    
                    #print "   "+"\033[1;47;30m------------------------------\033[0m"
                    print "   "+"\033[1;47;31m  ASM Weapon Package Summary  \033[0m"
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mShip Name of Origin:          \033[0m" +" "+shipName
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mTarget Position:              \033[0m"+" "+ str([targetX,targetY])
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mDistance to Target            \033[0m"+" "+str(distancetoTarget)
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mPoints left after Launch:     \033[0m"+" "+str(self.points - points)
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mMissle Flight Time:           \033[0m"+" "+str(int(distancetoTarget/6))
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mASM Missles Left after Launch:\033[0m"+" "+str(self.player2Ships[count].ASM - 1)
                    print "   "+"\033[1;47;30m------------------------------\033[0m"
                    print " "
                    while(True):#ask user if he wants to retaliate
                        launchCode = raw_input("\033[5;41;37mDo you wish to proceed with ASM Missle Launch? (yes/no):\033[0m" + " ")
                        print " "
                        if(launchCode == "yes"):
                            print "   "+"\033[1;41;37m---Entering Snap Count---\033[0m"
                            print "           ."
                            time.sleep(1)
                            print "   "+"\033[1;41;37m---Missle Armed---\033[0m"
                            print "           ."
                            time.sleep(1)
                            print "   "+"\033[1;41;37m---MISSLE AWAY---\033[0m"
                            for h in range(0,int(distancetoTarget/6)):
                                print "           ."
                                time.sleep(1)
                            break
                        elif(launchCode == "no"):
                            print "ASM Missle Battery is Standing Down."
                            return False
                        else:
                            print "Reenter valid information."
            
                    
                    self.ASMflag = 1#for HARM
                    if(self.player2Ships[count].position[1] not in self.ASMposition):#record where last ASM missle came from
                        self.ASMposition.append(self.player2Ships[count].position[1])
                    self.points = self.points - points#take points
                    self.player2Ships[count].ASM = self.player2Ships[count].ASM - 1#loses a missle
                    if(distancetoTarget<=10):
                        hit = 1 #100% change of hitting
                    else:
                        percentage = int(30 + (80*(50-distancetoTarget)/50))#chance of hitting if over 10 distance
                    
                        percentList = []
                        for y in range(0,percentage):
                            percentList.append(1)
                        for y in range(percentage, 100):
                            percentList.append(0)
                        randNum = random.randrange(0,99,1)#random number generator between 0 and 99 and increasing by 1
                        if(percentList[randNum] == 1):
                            hit = 1
                        else:
                            hit = 0
                            #time.sleep(2)#wait 2 seconds
                            print "          "+"\033[1;44;37mMiss\033[0m"#print miss"
                            print " "
                            self.removeDeadShip()
                            return
                    if(hit == 1):
                        for y in range(0,len(self.player1Ships)):
                            if([targetX,targetY] in self.player1Ships[y].position):
                                self.player1Ships[y].health = self.player1Ships[y].health-self.ASMfixedDamage-random.randrange(0,self.ASMvariableDamage,1)#20(fixed)+20(rand)
                                #time.sleep(2)#wait 2 seconds
                                print  "          "+"\033[1;41;37mHit\033[0m"#print hit
                                print " "
                                self.removeDeadShip()
                                return
                        #time.sleep(2)#wait 2 seconds
                        print  "          "+"\033[1;44;37mMiss\033[0m"#print miss
                        print " "
                        self.removeDeadShip()
                        return

                elif(weapon == "HARM"):
                    self.points = self.points - points
                    self.player2Ships[count].HARM = self.player2Ships[count].HARM - 1#loses a missle
                    self.ASMflag = 0
                    self.ASMposition = []
                    for y in range(0,len(self.player1Ships)):
                        if([targetX,targetY] in self.player1Ships[y].position):
                            print "   "+"\033[1;41;37mMISSLE AWAY\033[0m"
                            self.player1Ships[y].health = self.player1Ships[y].health-self.HARMfixedDamage-random.randrange(0,self.HARMvariableDamage,1)#20(fixed)+10(rand)
                            for e in range(0,2):
                                time.sleep(1)#wait 2 seconds
                                print "        ."
                            print "       "+"\033[1;41;37mHit\033[0m"#print hit
                            print " "
                            self.removeDeadShip()
                            return
                    print "\033[1;41;37mMISSLE AWAY\033[0m"
                    for e in range(0,2):
                        time.sleep(1)#wait 2 seconds
                        print "        ."
                    print "       "+"\033[1;44;37mMiss\033[0m"#print miss
                    print " "
                    self.removeDeadShip()
                    return
                
                elif(weapon == "SRM"):
                    
                    self.beforeFireMap(player,shipName,targetX,targetY)
                    print " "
                    while(True):#ask user if he wants to retaliate
                        mapCode = raw_input("\033[1;41;37mDo you wish to engage? You will have one more chance to cancel. (yes/no):\033[0m" + " ")
                        print " "
                        if(mapCode == "yes"):
                            print "   "+"\033[1;41;37m---Proceed to Weapon Summary---\033[0m"
                            print "           ."
                            print "           ."
                            print "           ."
                            print "           ."
                            print "           ."
                            #time.sleep(1)
                            break
                        elif(mapCode == "no"):
                            print "SRM Missle Battery is Standing Down."
                            return False
                        else:
                            print "Reenter valid information."
            

                    print "   "+"\033[1;47;31m  SRM Weapon Package Summary  \033[0m"
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mShip Name of Origin:          \033[0m" +" "+shipName
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mTarget Position:              \033[0m"+" "+ str([targetX,targetY])
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mDistance to Target            \033[0m"+" "+str(distancetoTarget)
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mPoints left after Launch:     \033[0m"+" "+str(self.points - points)
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mMissle Flight Time:           \033[0m"+" "+str(int(distancetoTarget/6))
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mASM Missles Left after Launch:\033[0m"+" "+str(self.player2Ships[count].SRM - 1)
                    print "   "+"\033[1;47;30m------------------------------\033[0m"
                    print " "
                    while(True):#ask user if he wants to retaliate
                        launchCode = raw_input("\033[5;41;37mDo you wish to proceed with SRM Missle Launch? (yes/no):\033[0m" + " ")
                        print " "
                        if(launchCode == "yes"):
                            time.sleep(1)
                            print "   "+"\033[1;41;37m---MISSLE AWAY---\033[0m"
                            for h in range(0,1):
                                print "           ."
                                time.sleep(1)
                            break
                        elif(launchCode == "no"):
                            print "SRM Missle Battery is Standing Down."
                            return False
                        else:
                            print "Reenter valid information."
            
                    
                    self.points = self.points - points
                    self.player2Ships[count].SRM = self.player2Ships[count].SRM - 1#loses a missle
                    for y in range(0,len(self.player1Ships)):
                        if([targetX,targetY] in self.player1Ships[y].position):
                            self.player1Ships[y].health = self.player1Ships[y].health-self.SRMfixedDamage-random.randrange(0,self.SRMvariableDamage,1)#10(fixed)+10(rand)
                            #time.sleep(2)#wait 2 seconds
                            print "          "+"\033[1;41;37mHit\033[0m"#print hit
                            print " "
                            self.removeDeadShip()
                            return
                    #time.sleep(2)#wait 2 seconds
                    print "          "+"\033[1;44;37mMiss\033[0m"#print miss
                    print " "
                    self.removeDeadShip()
                    return
        
                else:#Planes -- limitless ammo

                    self.beforeFireMap(player,shipName,targetX,targetY)
                    print " "
                    while(True):#ask user if he wants to retaliate
                        mapCode = raw_input("\033[1;41;37mDo you wish to engage? You will have one more chance to cancel. (yes/no):\033[0m" + " ")
                        print " "
                        if(mapCode == "yes"):
                            print "   "+"\033[1;41;37m---Proceed to Weapon Summary---\033[0m"
                            print "           ."
                            print "           ."
                            print "           ."
                            print "           ."
                            print "           ."
                            #time.sleep(1)
                            break
                        elif(mapCode == "no"):
                            print "All Planes are Standing Down."
                            return False
                        else:
                            print "Reenter valid information."
            


                    print "   "+"\033[1;47;31m    Planes Weapon Summary     \033[0m"
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mShip Name of Origin:          \033[0m" +" "+shipName
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mTarget Position:              \033[0m"+" "+ str([targetX,targetY])
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mDistance to Target            \033[0m"+" "+str(distancetoTarget)
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mPoints left after Launch:     \033[0m"+" "+str(self.points - points)
                    print "   "+"------------------------------"
                    print "   "+"\033[1;41;37mMissle Flight Time:           \033[0m"+" "+str(int(distancetoTarget/6))
                    print "   "+"\033[1;47;30m------------------------------\033[0m"
                    print " "
                    while(True):#ask user if he wants to retaliate
                        launchCode = raw_input("\033[5;41;37mDo you wish to deploy your fighters? (yes/no):\033[0m" + " ")
                        print " "
                        if(launchCode == "yes"):
                            time.sleep(1)
                            print "   "+"\033[1;41;37m---PLANES AWAY---\033[0m"
                            for h in range(0,1):
                                print "           ."
                                time.sleep(1)
                            break
                        elif(launchCode == "no"):
                            print "All Planes are Standing Down."
                            return False
                        else:
                            print "Reenter valid information."
            
                    
                    self.points = self.points - points
                    for y in range(0,len(self.player1Ships)):
                        if([targetX,targetY] in self.player1Ships[y].position):
                            self.player1Ships[y].health = self.player1Ships[y].health-self.PlanesfixedDamage-random.randrange(0,self.PlanesvariableDamage,1)#10(fixed)+20(rand)
                            #time.sleep(2)#wait 2 seconds
                            print "          "+"\033[1;41;37mHit\033[0m" #print hit
                            print " "
                            self.removeDeadShip()
                            return
                    #time.sleep(2)#wait 2 seconds
                    print "          "+"\033[1;44;37mMiss\033[0m"#print miss
                    print " "
                    self.removeDeadShip()
                    return
        
            else:#not enough points
                print "Not enough points to engage."
                print " "
                return False
            
    def clearScreen(self,numLines):
        #clears the screen by printing as many numLines

        for x in range(0,numLines):
            print " "

    def status(self,player):
        #prints the status of all ships
        
        print "\033[1;47;30mPlayer:\033[0m" + " " + str(self.player)
        print "\033[1;47;30mPoints left in turn:\033[0m" + " " + str(self.points)
        print " "
        if(player == "Player1"):
            for x in range(0, len(self.player1Ships)):
                if(type(self.player1Ships[x]) is Carrier):
                    healthPerc = int((((self.player1Ships[x].health)/100.0)*100))
                if(type(self.player1Ships[x]) is Destroyer):
                    healthPerc = int((((self.player1Ships[x].health)/60.0)*100))
                if(type(self.player1Ships[x]) is Patrol):
                    healthPerc = int((((self.player1Ships[x].health)/30.0)*100))
                if(healthPerc >= 70 and (type(self.player1Ships[x]) is Destroyer)):#greater than 70% health and destroyer
                    print "\033[1;42;37mShip Name  Health  ASM  HARM  SRM  \033[0m"
                    print "    "+self.player1Ships[x].name+"       "+str(self.player1Ships[x].health)+"     "+str(self.player1Ships[x].ASM)+"    "+str(self.player1Ships[x].HARM)+"     "+str(self.player1Ships[x].SRM)

                elif(healthPerc >= 70 and ((type(self.player1Ships[x]) is Carrier) or (type(self.player1Ships[x]) is Patrol))):#greater than 70% health and carrier or patrol
                    print "\033[1;42;37mShip Name  Health  ASM  HARM  SRM  \033[0m"
                    print "    "+self.player1Ships[x].name+"       "+str(self.player1Ships[x].health)+"     "+"X"+"    "+"X"+"     "+"X"
                    
                elif(healthPerc < 70 and healthPerc >= 40 and (type(self.player1Ships[x]) is Destroyer)):#less than 70% but greater than 40 and is destroyer
                    print "\033[1;43;37mShip Name  Health  ASM  HARM  SRM  \033[0m"
                    print "    "+self.player1Ships[x].name+"       "+str(self.player1Ships[x].health)+"     "+str(self.player1Ships[x].ASM)+"    "+str(self.player1Ships[x].HARM)+"     "+str(self.player1Ships[x].SRM)

                elif(healthPerc < 70 and healthPerc >= 40 and ((type(self.player1Ships[x]) is Carrier) or (type(self.player1Ships[x]) is Patrol))):#less than 70% but greater than 40%health and carrier or patrol
                    print "\033[1;43;37mShip Name  Health  ASM  HARM  SRM  \033[0m"
                    print "    "+self.player1Ships[x].name+"       "+str(self.player1Ships[x].health)+"     "+"X"+"    "+"X"+"     "+"X"
                    
                elif(healthPerc < 40 and (type(self.player1Ships[x]) is Destroyer)):#less than 40 and is destroyer
                    print "\033[5;41;37mShip Name  Health  ASM  HARM  SRM  \033[0m"
                    print "    "+self.player1Ships[x].name+"       "+str(self.player1Ships[x].health)+"     "+str(self.player1Ships[x].ASM)+"    "+str(self.player1Ships[x].HARM)+"     "+str(self.player1Ships[x].SRM)

                else:#patrol or carrier with health under 40%
                    print "\033[5;41;37mShip Name  Health  ASM  HARM  SRM  \033[0m"
                    print "    "+self.player1Ships[x].name+"       "+str(self.player1Ships[x].health)+"     "+"X"+"    "+"X"+"     "+"X"
                    
            for x in range(0,len(self.player1DeadShips)):#Dead Ships
                if((type(self.player1DeadShips[x]) is Destroyer)):
                    print "\033[1;41;37mShip Name  Health  ASM  HARM  SRM  \033[0m"
                    print "    "+self.player1DeadShips[x].name+"       "+"0"+"     "+str(self.player1DeadShips[x].ASM)+"    "+str(self.player1DeadShips[x].HARM)+"     "+str(self.player1DeadShips[x].SRM)

                else:#(((type(self.player1DeadShips[x]) is Carrier) or (type(self.player1DeadShips[x]) is Patrol))):
                    print "\033[1;41;37mShip Name  Health  ASM  HARM  SRM  \033[0m"
                    print "    "+self.player1DeadShips[x].name+"       "+"0"+"     "+"X"+"    "+"X"+"     "+"X"
                    

        
        else:#(player == "Player2"):
            for x in range(0, len(self.player2Ships)):
                if(type(self.player2Ships[x]) is Carrier):
                    healthPerc = int((((self.player2Ships[x].health)/100.0)*100))
                if(type(self.player2Ships[x]) is Destroyer):
                    healthPerc = int((((self.player2Ships[x].health)/60.0)*100))
                if(type(self.player2Ships[x]) is Patrol):
                    healthPerc = int((((self.player2Ships[x].health)/30.0)*100))
                    
                #print healthPerc
                if(healthPerc >= 70 and (type(self.player2Ships[x]) is Destroyer)):#greater than 70% health and destroyer
                    print "\033[1;42;37mShip Name  Health  ASM  HARM  SRM  \033[0m"
                    print "    "+self.player2Ships[x].name+"       "+str(self.player2Ships[x].health)+"     "+str(self.player2Ships[x].ASM)+"    "+str(self.player2Ships[x].HARM)+"     "+str(self.player2Ships[x].SRM)

                elif(healthPerc >= 70 and ((type(self.player2Ships[x]) is Carrier) or (type(self.player2Ships[x]) is Patrol))):#greater than 70% health and carrier or patrol
                    print "\033[1;42;37mShip Name  Health  ASM  HARM  SRM  \033[0m"
                    print "    "+self.player2Ships[x].name+"       "+str(self.player2Ships[x].health)+"     "+"X"+"    "+"X"+"     "+"X"
                    
                elif(healthPerc < 70 and healthPerc >= 40 and (type(self.player2Ships[x]) is Destroyer)):#less than 70% but greater than 40 and is destroyer
                    print "\033[1;43;37mShip Name  Health  ASM  HARM  SRM  \033[0m"
                    print "    "+self.player2Ships[x].name+"       "+str(self.player2Ships[x].health)+"     "+str(self.player2Ships[x].ASM)+"    "+str(self.player2Ships[x].HARM)+"     "+str(self.player2Ships[x].SRM)

                elif(healthPerc < 70 and healthPerc >= 40 and ((type(self.player2Ships[x]) is Carrier) or (type(self.player2Ships[x]) is Patrol))):#less than 70% but greater than 40%health and carrier or patrol
                    print "\033[1;43;37mShip Name  Health  ASM  HARM  SRM  \033[0m"
                    print "    "+self.player2Ships[x].name+"       "+str(self.player2Ships[x].health)+"     "+"X"+"    "+"X"+"     "+"X"
                    
                elif(healthPerc < 40 and (type(self.player2Ships[x]) is Destroyer)):#less than 40 and is destroyer
                    print "\033[5;41;37mShip Name  Health  ASM  HARM  SRM  \033[0m"
                    print "    "+self.player2Ships[x].name+"       "+str(self.player2Ships[x].health)+"     "+str(self.player2Ships[x].ASM)+"    "+str(self.player2Ships[x].HARM)+"     "+str(self.player2Ships[x].SRM)

                else:#patrol or carrier with health under 40%
                    print "\033[5;41;37mShip Name  Health  ASM  HARM  SRM  \033[0m"
                    print "    "+self.player2Ships[x].name+"       "+str(self.player2Ships[x].health)+"     "+"X"+"    "+"X"+"     "+"X"
                    
            for x in range(0,len(self.player2DeadShips)):#Dead Ships
                if((type(self.player2DeadShips[x]) is Destroyer)):
                    print "\033[1;41;37mShip Name  Health  ASM  HARM  SRM  \033[0m"
                    print "    "+self.player2DeadShips[x].name+"       "+"0"+"     "+str(self.player2DeadShips[x].ASM)+"    "+str(self.player2DeadShips[x].HARM)+"     "+str(self.player2DeadShips[x].SRM)

                else:#(((type(self.player1DeadShips[x]) is Carrier) or (type(self.player1DeadShips[x]) is Patrol))):
                    print "\033[1;41;37mShip Name  Health  ASM  HARM  SRM  \033[0m"
                    print "    "+self.player2DeadShips[x].name+"       "+"0"+"     "+"X"+"    "+"X"+"     "+"X"
                    


    def historyPrint(self,player):
        #prints the complete history of enemy ships that have been spotted by player
        
        for x in range(0,1):#print spaces
            print " "

        if(player == "Player1"):
            field =[[0 for j in range(self.sizeFieldx)] for i in range(self.sizeFieldy)]
            for y in range (0,self.sizeFieldy):
                for x in range (0,self.sizeFieldx):
                    field[y][x] = x
                    
            enemySym = '\033[93m'#yellow
            endSym = '\033[0m'
            for x in range(0,len(self.player1History)):
                field[self.player1History[x][1]][self.player1History[x][0]] = enemySym + "EE" + endSym
            
        
            yAxisPlaceHolders = [0 for i in range(self.sizeFieldy)]
            for y in range(0,self.sizeFieldy):
                yAxisPlaceHolders[y] = y
            for y in range (0,self.sizeFieldy):
                if(y<10):
                    print str(yAxisPlaceHolders[y])+"||",
                else:
                    print str(yAxisPlaceHolders[y])+"|",
                for x in range(0,self.sizeFieldx):
                    if(x < self.sizeFieldx-1 and not isinstance(field[y][x],basestring)):
                        if(x<10):
                            print str(field[y][x])+"|",
                        else:
                            print str(field[y][x]),
                    elif(x < self.sizeFieldx-1 and isinstance(field[y][x],basestring)):
                        print str(field[y][x]),
                    else:
                        print str(field[y][x])

        else:#player2
            field =[[0 for j in range(self.sizeFieldx)] for i in range(self.sizeFieldy)]
            for y in range (0,self.sizeFieldy):
                for x in range (0,self.sizeFieldx):
                    field[y][x] = x
                    
            enemySym = '\033[93m'#yellow
            endSym = '\033[0m'
            for x in range(0,len(self.player2History)):
                field[self.player2History[x][1]][self.player2History[x][0]] = enemySym + "EE" + endSym
            
        
            yAxisPlaceHolders = [0 for i in range(self.sizeFieldy)]
            for y in range(0,self.sizeFieldy):
                yAxisPlaceHolders[y] = y
            for y in range (0,self.sizeFieldy):
                if(y<10):
                    print str(yAxisPlaceHolders[y])+"||",
                else:
                    print str(yAxisPlaceHolders[y])+"|",
                for x in range(0,self.sizeFieldx):
                    if(x < self.sizeFieldx-1 and not isinstance(field[y][x],basestring)):
                        if(x<10):
                            print str(field[y][x])+"|",
                        else:
                            print str(field[y][x]),
                    elif(x < self.sizeFieldx-1 and isinstance(field[y][x],basestring)):
                        print str(field[y][x]),
                    else:
                        print str(field[y][x])

                        
    def retaliateHARM(self,player):
        #This function warns the opponent if a HARM missle has been fired within 15 spaces of any of his destroyers(if that destroyer has HARM missles)
        #It then gives the user the option to retaliate, by giving the user the position of the place where the ASM was fired and ending the users turn.
        #It also updates the history of the user.

        if(self.ASMflag == 0):
            return False
        if(player == "Player1"):
            if(self.ASMflag == 1):#check if destroyer is within 15 spaces of ASM shot
                destroyerHARMList = []
                destroyerList = []
                oneFlag = 0
                for x in range(0,len(self.player1Ships)):
                    if(type(self.player1Ships[x]) is Destroyer):
                        individualList = []
                        destroyerList.append(self.player1Ships[x])#make a destroyer list
                        for y in range(0,len(self.ASMposition)):
                            distance = int(pow(pow(self.player1Ships[x].position[1][0] - self.ASMposition[y][0],2) + pow(self.player1Ships[x].position[1][1] - self.ASMposition[y][1],2),0.5))
                            #print distance
                            if(distance <= 15 and self.player1Ships[x].HARM > 0):#distance under 15 and has HARM Missles
                                individualList.append(1)
                                oneFlag = 1
                            else:
                                individualList.append(0)
                        destroyerHARMList.append(individualList)

            
            if(oneFlag == 0):
                return False
            
            self.radarFind(player)#So player can see map before deciding
            print " "
            while(True):#ask user if he wants to retaliate
                retaliate = raw_input("\033[1;44;37mEnemy ASM missle detected. Do you wish to retaliate? (yes/no):\033[0m" + " ")
                if(retaliate == "yes"):
                    break
                elif(retaliate == "no"):
                    self.ASMflag = 0#take down the flag
                    self.ASMposition = []#empty array
                    print "No retaliation."
                    print " "
                    return False
                else:
                    print "Reenter valid information."
            
            self.radarFind("Player1")
            print " "
            #####History
            seeList = []#for history later
            for g in range(0,len(self.ASMposition)):
                seeList.append(0)#initilize to 0
            for g in range(0,len(destroyerHARMList)):
                for u in range(0,len(self.ASMposition)):
                    if(destroyerHARMList[g][u] == 1):
                        seeList[u] = 1
            for g in range(0,len(self.ASMposition)):
                if(seeList[g] == 1 and (self.ASMposition[g] not in self.player1History)):
                    self.player1History.append(self.ASMposition[g])
            #print seeList
            ########################

            #print destroyerHARMList
            for x in range(0,len(destroyerList)):
                print " "
                print "\033[1;44;37mDestroyer,\033[0m"+ " " +destroyerList[x].name+" " +"\033[1;44;37m can retaliate on enemy ship(s) at location(s): \033[0m",
                for y in range(0,len(destroyerHARMList[x])):
                    if(destroyerHARMList[x][y] == 1):
                        print self.ASMposition[y],
                        print ": ",
                    else:
                        print "XXXX: ",

            print " "
            print " "
            position = 100#dummy variable, just initializing
            while(True):#ask user which ship to retaliate with
                whichShip = raw_input("\033[1;44;37mWhich Ship do you want to retaliate with:\033[0m" + " ")
                print " "
                for z in range(0,len(destroyerList)):#Check if ship exists
                    if(whichShip == destroyerList[z].name):
                        inList = 1
                        position = z
                        break
                    else:
                        inList = 0
                if(position == 100):#means that name wasn't found
                    print "Ship Doesn't exist. Reenter valid information."
                    print " "
                else:    
                    for z in range(0,len(destroyerHARMList[position])):
                        if(destroyerHARMList[position][z] == 1):#can ship retaliate
                            canRetaliate = 1
                            break
                        else:
                            canRetaliate = 0
                                   
                if(inList == 1 and canRetaliate == 1):
                    break
                elif(position == 100):
                    print " "
                else:
                    print "This ship can't retaliate against any targets. Reenter valid information."
                    print " "

            while(True):#ask user which target the ship would like to retaliate against
                try:
                    whichPosition = int(raw_input("\033[1;44;37mWhich Ship do you want to retaliate against (0,1,2...ec.):\033[0m" + " "))
                    print " "
                    if(whichPosition > len(destroyerHARMList[position]) - 1):
                        print "Invalid value. Reenter Valid Information."
                        print " "
                    else:
                        if(destroyerHARMList[position][whichPosition] == 0):
                            print "This Ship cannot retaliate against this position. Reenter valid information."
                            print " "
                        else:#equals 1 so can retaliate
                            targetX = self.ASMposition[whichPosition][0]
                            targetY = self.ASMposition[whichPosition][1]
                            self.weaponsPackage(player,whichShip,"HARM",targetX,targetY)
                            self.ASMflag = 0#take down the flag
                            self.ASMposition = []#empty array
                            return
                        
                except ValueError:
                    print("Input not Valid! Reenter information.")
                    print " "
                                   
        
        else:#player2
            if(self.ASMflag == 1):#check if destroyer is within 15 spaces of ASM shot
                destroyerHARMList = []
                destroyerList = []
                oneFlag = 0
                for x in range(0,len(self.player2Ships)):
                    if(type(self.player2Ships[x]) is Destroyer):
                        individualList = []
                        destroyerList.append(self.player2Ships[x])#make a destroyer list
                        for y in range(0,len(self.ASMposition)):
                            distance = int(pow(pow(self.player2Ships[x].position[1][0] - self.ASMposition[y][0],2) + pow(self.player2Ships[x].position[1][1] - self.ASMposition[y][1],2),0.5))
                            #print distance
                            if(distance <= 15 and self.player2Ships[x].HARM > 0):#distance under 15 and has HARM Missles
                                individualList.append(1)
                                oneFlag = 1
                            else:
                                individualList.append(0)
                        destroyerHARMList.append(individualList)
            
            if(oneFlag == 0):
                return False
            
            self.radarFind(player)#So player can see map before deciding
            print " "
            while(True):#ask user if he wants to retaliate
                retaliate = raw_input("\033[1;44;37mEnemy ASM missle detected. Do you wish to retaliate? (yes/no):\033[0m" + " ")
                if(retaliate == "yes"):
                    print " "
                    break
                elif(retaliate == "no"):
                    self.ASMflag = 0#take down the flag
                    self.ASMposition = []#empty array
                    print "No retaliation."
                    print " "
                    return False
                else:
                    print "Reenter valid information."
            
            self.radarFind("Player2")
            print " "
            #####History
            seeList = []#for history later
            for g in range(0,len(self.ASMposition)):
                seeList.append(0)#initilize to 0
            for g in range(0,len(destroyerHARMList)):
                for u in range(0,len(self.ASMposition)):
                    if(destroyerHARMList[g][u] == 1):
                        seeList[u] = 1
            for g in range(0,len(self.ASMposition)):
                if(seeList[g] == 1 and (self.ASMposition[g] not in self.player2History)):
                    self.player2History.append(self.ASMposition[g])
            #print seeList
            #self.historyPrint("Player2")
            ########################

            #print destroyerHARMList
            for x in range(0,len(destroyerList)):
                print " "
                print "\033[1;44;37mDestroyer,\033[0m"+ " " +destroyerList[x].name+" " +"\033[1;44;37m can retaliate on enemy ship(s) at location(s): \033[0m",
                for y in range(0,len(destroyerHARMList[x])):
                    if(destroyerHARMList[x][y] == 1):
                        print self.ASMposition[y],
                        print ": ",
                    else:
                        print "XXXX: ",

            print " "
            print " "
            position = 100#dummy variable, just initializing
            while(True):#ask user which ship to retaliate with
                whichShip = raw_input("\033[1;44;37mWhich Ship do you want to retaliate with:\033[0m" + " ")
                print " "
                for z in range(0,len(destroyerList)):#Check if ship exists
                    if(whichShip == destroyerList[z].name):
                        inList = 1
                        position = z
                        break
                    else:
                        inList = 0
                if(position == 100):#means that name wasn't found
                    print "Ship Doesn't exist. Reenter valid information."
                    print " "
                else:    
                    for z in range(0,len(destroyerHARMList[position])):
                        if(destroyerHARMList[position][z] == 1):#can ship retaliate
                            canRetaliate = 1
                            break
                        else:
                            canRetaliate = 0
                                   
                if(inList == 1 and canRetaliate == 1):
                    break
                elif(position == 100):
                    print " "
                else:
                    print "This ship can't retaliate against any targets. Reenter valid information."
                    print " "

            while(True):#ask user which target the ship would like to retaliate against
                try:
                    whichPosition = int(raw_input("\033[1;44;37mWhich Ship do you want to retaliate against (0,1,2...ec.):\033[0m" + " "))
                    print " "
                    if(whichPosition > len(destroyerHARMList[position]) - 1):
                        print "Invalid value. Reenter Valid Information."
                        print " "
                    else:
                        if(destroyerHARMList[position][whichPosition] == 0):
                            print "This Ship cannot retaliate against this position. Reenter valid information."
                            print " "
                        else:#equals 1 so can retaliate
                            targetX = self.ASMposition[whichPosition][0]
                            targetY = self.ASMposition[whichPosition][1]
                            self.weaponsPackage(player,whichShip,"HARM",targetX,targetY)
                            #self.status("Player1")
                            #print"----------"
                            #self.status("Player2")
                            self.ASMflag = 0#take down the flag
                            self.ASMposition = []#empty array
                            return
                        
                except ValueError:
                    print("Input not Valid! Reenter information.")
                    print " "
                                  
                             
    def endturn(self):
        while(True):
            endturnInput = raw_input("\033[1;47;30mDo you wish to end your turn? (yes/no)\033[0m"+" ")
            if(endturnInput == "yes"):
                self.points = 7#new turn points

                if(self.player == 1):
                    self.player = 2
                else:#self.player = 2
                    self.player = 1
                
                self.clearScreen(300)
                while(True):
                    newturn = raw_input("\033[1;47;30mNew Player, do you wish to start your turn? (yes)\033[0m"+" ")
                    if(newturn == "yes"):
                        self.clearScreen(80)
                        return True
                    else:
                        print "Invalid input."

            elif(endturnInput == "no"):
                print "Turn not ended."
                print " "
                return False

            else:
                print "Invalid input. Reenter valid information."
                
            
#"""
    def gameMaster(self):
        #This function runs the game

        self.clearScreen(80)
        #Initilize the game for player 1 and allow them to pick number of ships
        self.player = 1 #player1's turn
        player = "Player1"
        self.points = 21#points used to get ships
        while(True):
            try:#choose number of carriers
                numCarrier = int(raw_input(player + " "+"\033[1;47;30mEnter number of Carriers (7 points)--\033[0m" +" "+ str(self.points) + " " + "\033[1;47;30mpoints left:\033[0m" + " "))
                print " "
                if(self.checkPoints(numCarrier*7)):
                    self.points = self.points - (numCarrier*7)
                    break
                else:
                    print "Not enough points."
            except ValueError:
                print("Input not Valid! Reenter information.")
         
        while(True):
            try:#choose number of destroyers
                numDest = int(raw_input(player + " " + "\033[1;47;30mEnter number of Destroyers (4 points)--\033[0m" + " "+str(self.points) + " " + "\033[1;47;30mpoints left:\033[0m" + " "))
                print " "
                if(self.checkPoints(numDest*4)):
                    self.points = self.points - (numDest*4)
                    break
                else:
                    print "Not enough points."
            except ValueError:
                print("Input not Valid! Reenter information.")

        while(True):
            try:#choose number of patrol boats
                numPat = int(raw_input(player + " " +"\033[1;47;30mEnter number of Patrol Boats (1 points)--\033[0m" +" "+ str(self.points) + " "+"\033[1;47;30m points left:\033[0m"+" "))
                print " "
                if(self.checkPoints(numPat)):
                    self.points = self.points - (numPat*1)
                    break
                else:
                    print "Not enough points."
            except ValueError:
                print("Input not Valid! Reenter information.")
                
        carrierNames = ["C1","C2","C3"]
        destNames = ["D1","D2","D3","D4","D5","D6"]
        patrolNames = ["P1","P2","P3","P4","P5","P6","P7","P8","P9","P10","P11","P12","P13","P14","P15","P16","P17","P18","P19","P20","P21"]

        for x in range(0,numCarrier):#give carrier names and add to list
            self.player1Ships.append(Carrier(carrierNames[x]))

        for x in range(0,numDest):#give destroyers range and add to list
            self.player1Ships.append(Destroyer(destNames[x]))

        for x in range(0,numPat):#give patrols names and add to list
            self.player1Ships.append(Patrol(patrolNames[x]))
       
        self.printEmptyField()#print empty field so viewer can see
        print " "
        for x in range(0,len(self.player1Ships)):#user input to position the ships
            if(type(self.player1Ships[x]) is Carrier):
                shipType = "carrier"
            elif(type(self.player1Ships[x]) is Destroyer):
                shipType = "destroyer"
            else:#patrol
                shipType = "patrol"
            shipP1pos=self.masterInput(self.player1Ships[x].name,player,shipType)
            self.player1Ships[x].position = shipP1pos
            self.printField(player)
            print " "

        #check to pass over to player 2
        while(True):
            passUser = raw_input("\033[1;47;30mDo you wish to end you turn and pass computer to Player 2? (yes):\033[0m" + " ")
            if(passUser == "yes"):
                print " "
                break
            else:
                print "Reenter valid input."
            
        ###Initialize player2
        self.clearScreen(80)
        #Initilize the game for player 2 and allow them to pick number of ships
        self.player = 2 #player1's turn
        player = "Player2"
        self.points = 21#points used to get ships
        while(True):
            try:#choose number of carriers
                numCarrier = int(raw_input(player + " " +"\033[1;47;30mEnter number of Carriers (7 points)--\033[0m" + " "+str(self.points) + " "+"\033[1;47;30m points left:\033[0m" + " "))
                print " "
                if(self.checkPoints(numCarrier*7)):
                    self.points = self.points - (numCarrier*7)
                    break
                else:
                    print "Not enough points."
            except ValueError:
                print("Input not Valid! Reenter information.")
         
        while(True):
            try:#choose number of destroyers
                numDest = int(raw_input(player + " " + "\033[1;47;30mEnter number of Destroyers (4 points)--\033[0m" +" "+ str(self.points) + " "+"\033[1;47;30m points left:\033[0m" + " "))
                print " "
                if(self.checkPoints(numDest*4)):
                    self.points = self.points - (numDest*4)
                    break
                else:
                    print "Not enough points."
            except ValueError:
                print("Input not Valid! Reenter information.")

        while(True):
            try:#choose number of patrol boats
                numPat = int(raw_input(player + " "+"\033[1;47;30mEnter number of Patrol Boats (1 points)--\033[0m" + " "+str(self.points) + " " +"\033[1;47;30m points left:\033[0m"+" "))
                print " "
                if(self.checkPoints(numPat)):
                    self.points = self.points - (numPat*1)
                    break
                else:
                    print "Not enough points."
            except ValueError:
                print("Input not Valid! Reenter information.")
                
        carrierNames = ["C1","C2","C3"]
        destNames = ["D1","D2","D3","D4","D5","D6"]
        patrolNames = ["P1","P2","P3","P4","P5","P6","P7","P8","P9","P10","P11","P12","P13","P14","P15","P16","P17","P18","P19","P20","P21"]

        for x in range(0,numCarrier):#give carrier names and add to list
            self.player2Ships.append(Carrier(carrierNames[x]))

        for x in range(0,numDest):#give destroyers range and add to list
            self.player2Ships.append(Destroyer(destNames[x]))

        for x in range(0,numPat):#give patrols names and add to list
            self.player2Ships.append(Patrol(patrolNames[x]))
       
        self.printEmptyField()#print empty field so viewer can see
        print " "
        for x in range(0,len(self.player2Ships)):#user input to position the ships
            if(type(self.player2Ships[x]) is Carrier):
                shipType = "carrier"
            elif(type(self.player2Ships[x]) is Destroyer):
                shipType = "destroyer"
            else:#patrol
                shipType = "patrol"
            shipP2pos=self.masterInput(self.player2Ships[x].name,player,shipType)
            self.player2Ships[x].position = shipP2pos
            self.printField(player)
            print " "

        #check to pass over to player 1 and begin game
        while(True):
            passUser = raw_input("\033[1;47;30mInitilization is over. Do you wish to pass computer to Player 1? (yes):\033[0m" + " ")
            if(passUser == "yes"):
                print " "
                break
            else:
                print "Reenter valid input."

        self.clearScreen(80)
        ############################################END of INITILIZATION -- BEGIN GAME############################################
        self.player = 1 #play begins with player 1
        self.points = 7
        
        while(True):
            #print "here"
            #print "Points: " + str(self.points)
            if(self.endgame == 1):
                print "\033[1;47;30mGAME OVER\033[0m"
            if(self.player == 1):
                player = "Player1"
            else:
                player = "Player2"
            self.retaliateHARM(player)#check if player can retaliate because of ASM shot in last turn
            self.ASMflag = 0
            self.ASMposition = []

            while(True):
                userInput = raw_input("\033[1;47;30mFleet standing by:\033[0m" + " ")

###############################################################            
                if(userInput == "clear"):
                    self.clearScreen(80)

################################################################
                elif(userInput == "end turn"):
                    status = self.endturn()
                    if(status == True):
                        break #if turn ended break out of this while loop

################################################################
                elif(userInput == "history"):
                    self.historyPrint(player)
                    print " "

###############################################################
                elif(userInput == "status"):
                    print " "
                    self.status(player)
                    print " "
############################################################                    
                elif(userInput == "map"):
                    self.radarFind(player)
                    print " "
############################################################
                elif(userInput == "show radar"):
                    self.allShipsRadar(player)
                    print " "
#############################################################
                elif(userInput == "come to course"):

                    shipName = raw_input("\033[1;47;30mWhich ship (or cancel):\033[0m" + " ")
                    variable = True
                    cancel = 0
                    if(shipName == "cancel"):
                        cancel = 1
                        variable = False
                    while(variable):
                        try:
                            course = raw_input("\033[1;47;30mWhat course (or cancel):\033[0m" + " ")
                            
                            if(course == "cancel"):
                                cancel = 1
                                break
                            course = int(course)
                            break
                        except ValueError:
                            print("Input not Valid! Reenter information.")
                    
                    if(cancel == 1):
                        cancel = 0
                        print "Canceled"
                        print " "
                    
                    else:
                        self.cometocourse(player,shipName,course)
                        print " "
#################################################################
                elif(userInput == "move"):
                    shipName = raw_input("\033[1;47;30mWhich ship (or cancel):\033[0m" + " ")
                    variable = True
                    cancel = 0
                    if(shipName == "cancel"):
                        cancel = 1
                        variable = False
                    
                    #if patrol
                    patrolNames = ["P1","P2","P3","P4","P5","P6","P7","P8","P9","P10","P11","P12","P13","P14","P15","P16","P17","P18","P19","P20","P21"]
                    if(shipName in patrolNames):
                        while(variable):
                            #variable = True
                            try:
                                patrolx = raw_input("\033[1;47;30mNew x position of patrol (or cancel):\033[0m" + " ")
                                if(patrolx == "cancel"):
                                    cancel = 1
                                    variable = False
                                    break
                                patrolx = int(patrolx)
                                break
                            except ValueError:
                                print "Input not Valid! Reenter information"
                                
                        while(variable):
                            try:
                                patroly = raw_input("\033[1;47;30mNew y position of patrol (or cancel):\033[0m" + " ")
                                if(patroly == "cancel"):
                                    cancel = 1
                                    break
                                patroly = int(patroly)
                                break
                            except ValueError:
                                print "Input not Valid! Reenter information"
                        
                        if(cancel == 1):
                            cancel = 0
                            print "Canceled"
                            print " "
                        
                        else:    
                            self.move(player,shipName,0,patrolx,patroly)
                            print " "


                    else:#not a patrol        
                        
                        while(variable):
                            try:
                                spaces = raw_input("\033[1;47;30mHow many spaces (or cancel):\033[0m" + " ")
                                if(spaces == "cancel"):
                                    cancel = 1
                                    variable = False
                                    break
                                spaces = int(spaces)
                                break
                            except ValueError:
                                print "Input not Valid! Reenter information"
                    
                        if(cancel == 1):
                            cancel = 0
                            print "Canceled"
                            print " "
                        
                        else:#regular (not patrol ship) move
                            self.move(player,shipName,spaces,0,0)
                            print " "

                    
########################################################################
 
                elif(userInput == "weapons package"):
                    shipName = raw_input("\033[1;47;30mWhich ship (or cancel):\033[0m" + " ")
                    variable = True
                    cancel = 0
                    if(shipName == "cancel"):
                        cancel = 1
                        variable = False
                    
                    if(cancel == 0):
                        weapon = raw_input("\033[1;47;30mWeapon (or cancel):\033[0m" + " ")
                        if(weapon == "cancel"):
                            cancel = 1
                            variable = False
                    while(variable):
                        try:
                            targetX = raw_input("\033[1;47;30mTarget x position (or cancel):\033[0m" + " ")
                            if(targetX == "cancel"):
                                cancel = 1
                                variable = False
                                break
                            targetX = int(targetX)
                            break
                        except ValueError:
                            print "Input not Valid! Reenter information"
                    
                    while(variable):
                        try:
                            targetY = raw_input("\033[1;47;30mTarget y position (or cancel):\033[0m" + " ")
                            if(targetY == "cancel"):
                                cancel = 1
                                break
                            targetY = int(targetY)
                            break
                        except ValueError:
                            print "Input not Valid! Reenter information"
                    
                    if(cancel == 1):
                        cancel = 0
                        print "Canceled"
                        print " "
                    elif(weapon == "HARM"):
                        print "HARM can only be used in retaliation to ASM missle."
                        print " "
                    else:
                        self.weaponsPackage(player,shipName,weapon,targetX,targetY)
                        print " "
#############################################################################
                else:
                    print "Command not recognized."
                    print " "
            
    
           #"""         
                   

def main():
    
    game1 = Game()
    game1.gameMaster()

if __name__ == "__main__":
    main()
