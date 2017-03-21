# -*- coding: cp1252 -*-
 
import threading
import Queue
import socket
import ast
from random import randint
import game
from weapon import Weapon

class GameLogic(threading.Thread):
    """
    Klasse zur Ausführung eines Spiels
    """

    def __init__(self, playerCount):
        """
        Initialisierung eines GameLogic
         
        Parameter:      int die maximale Spieleranzahl
        Rückgabewerte:  -
        """
        threading.Thread.__init__(self)
        self.deamon = True

        self.queue = Queue.Queue(0)

        self.playerCount = playerCount
        self.playerConnectedCount = 0
        self.players = []
        self.weaponPositions = []
        self.possibleWeaponPositions = ["140_110", "490_110", "420_300", "220_300", "060_300", "600_300", "420_550", "220_550", "090_490", "550_480", "600_170", "600_040", "350_050", "290_040", "050_180"]
        self.playerPositions = []
        self.game = game.Game(self)

        self.MCAST_GRP = '224.1.1.1'
        self.MCAST_PORT = 5000
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        
    def run(self):
        while True:
            data = self.queue.get()
            self.socket.sendto(data, (self.MCAST_GRP, self.MCAST_PORT))
            self.queue.task_done()
            self.game.updatePlayers(self.playerPositions)
     
    def addPlayer(self, player):
        """
        Hinzufügen eines Spielers, falls die maximale Spieleranzahl noch nicht erreicht wurde
         
        Parameter:      object servereigene Spielerrepreäsentation
        Rückgabewerte:  -
        """
        if self.playerCount>self.playerConnectedCount:
            self.players.append(player)
            self.playerPositions.append('000_000')
            self.playerConnectedCount += 1
            print('Player' + str(player) + 'connected, ' + str(self.playerConnectedCount) + '/' + str(self.playerCount) + ' connected')
            if self.playerCount==self.playerConnectedCount:
                self.startGame()
        else:
            print('{0} tried to connect, but there is no space for another player'.format(player))

    def startGame(self):
        self.weaponPositions.extend(self.possibleWeaponPositions[0:4])
        self.queue.put("Hello there. The game starts now.")
        self.queue.put("n." + str(self.players))
        self.game.setPlayerlist(self.players)
        self.game.setRandomWeapons(self.weaponPositions)

        self.start()
 
    def removePlayer(self, player):
        """
        Entfernen eines Spielers, falls er zuvor hinzugefügt wurde
         
        Parameter:      object servereigene Spielerrepreäsentation
        Rückgabewerte:  -
        """
        try:
            self._players.remove(player)
        except: pass
    
    def shoot(self, clickedPos, player):
        """
        Registrieren eines Schusses
         
        Parameter:      string Schussposition
                        object servereigene Spielerrepreäsentation
        Rückgabewerte:  -
        """
        shot = str(clickedPos) + ";" + str(player)
        self.game.shoot(clickedPos, player)
        self.queue.put("s." + shot)
        
    def updatePlayerPosition(self, newPosition, player):
        """
        Updaten einer Position
         
        Parameter:      string Spielerposition
                        object servereigene Spielerrepreäsentation
        Rückgabewerte:  -
        """
        index = self.players.index(player)
        self.playerPositions[index] = newPosition
  
        if self.queue.unfinished_tasks < 15:
            self.queue.put("p." + str(self.playerPositions))



    def updateWeapon(self, pos, playerName, room):
        print 'updateWeapon'
        newPos = self.createNewPos()
        self.sendWeapon(newPos, pos, playerName, room)
        
    def sendWeapon(self, newPos, oldPos, playerName, room):
        print 'sendWeapon'
        #der raum kommt nocht in die msg
        msg = str((str(oldPos[0]), str(oldPos[1]), newPos, str(playerName)))
        self.queue.put("w." + msg )
        print 'msg'
        oldPosition = self.convertPositionToString(oldPos)
        self.removeWeapon(oldPosition)
        self.game.changeWeapon(oldPos, newPos, room)
        self.weaponPositions.append(newPos)

    def sendStartWeapon(self, position, weaponParameter):
        msg = str((str(position[0]), str(position[1]), str(weaponParameter[0]), str(weaponParameter[1]), str(weaponParameter[2]), str(weaponParameter[3])))
        room = weaponParameter#wird evtl noch eingebracht... mal sehen
        self.queue.put("v." + msg)
        
    def removeWeapon(self, oldPos):
        self.weaponPositions.remove(oldPos)

    def createNewPos(self):
        index = randint(1,len(self.possibleWeaponPositions)-1)
        position = self.possibleWeaponPositions[index]
        while position in self.weaponPositions:
            index = randint(1,len(self.possibleWeaponPositions)-1)
            position = self.possibleWeaponPositions[index]
        return position

    def playerDied(self, player):
        """
        Wird aufgerufen, wenn ein Spieler stirbt.
        """
        index = self.players.index(player)
        self.players.pop(index)
        self.playerPositions.pop(index)
        self.playerCount -= 1
        self.playerConnectedCount -= 1
        
        self.queue.put("d." + str(player))

    def changeRoom(self, player, room, exitPoint):
        """
        Wird aufgerufen, wenn ein Spieler den Raum gewechselt hat.
        """
        print 'changeRoom, gameLogic'
        #alle doors und weapons schicken und ip
        index = self.players.index(player)
        self.playerPositions[index] =  exitPoint
        self.queue.put("r." + str(player) + "|"  + str(room) + "|"  + str(exitPoint))

        
    def convertPositionToString(self, position):
        '''
        bekommt eine Position eines Spieler und wandelt diese um
        bsp.: (12,7) -> "012_007"
        Parameter:      position
        return values:  convertedPosition, 7 Zeichen langer String der Position
        '''
        xPos = position[0]
        yPos = position[1]
        convertedPosition = str(xPos).zfill(3) + '_' + str(yPos).zfill(3)
        return convertedPosition
