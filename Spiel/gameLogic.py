# -*- coding: cp1252 -*-
 
import threading
import Queue
import socket
import game

class GameLogic(threading.Thread):
    """
    Klasse zur Ausf�hrung eines Spiels
    """

    def __init__(self, playerCount):
        """
        Initialisierung eines GameLogic
         
        Parameter:      int die maximale Spieleranzahl
        R�ckgabewerte:  -
        """
        threading.Thread.__init__(self)
        self.deamon = True

        self.queue = Queue.Queue(0)

        self.playerCount = playerCount
        self.playerConnectedCount = 0
        self.players = []
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
        Hinzuf�gen eines Spielers, falls die maximale Spieleranzahl noch nicht erreicht wurde
         
        Parameter:      object servereigene Spielerrepre�sentation
        R�ckgabewerte:  -
        """
        if self.playerCount>self.playerConnectedCount:
            self.players.append(player)
            self.playerPositions.append('000_000')
            self.playerConnectedCount += 1
            print('Player' + str(player) + 'connected, ' + str(self.playerConnectedCount) + '/' + str(self.playerCount) + ' connected')
            if self.playerCount==self.playerConnectedCount:
                self.queue.put("Hello there. The game starts now.")
                self.queue.put("n." + str(self.players))
                self.game.setPlayerlist(self.players)
                self.start()
        else:
            print('{0} tried to connect, but there is no space for another player'.format(player))

 
    def removePlayer(self, player):
        """
        Entfernen eines Spielers, falls er zuvor hinzugef�gt wurde
         
        Parameter:      object servereigene Spielerrepre�sentation
        R�ckgabewerte:  -
        """
        try:
            self._players.remove(player)
        except: pass
    
    def shoot(self, clickedPos, player):
        """
        Registrieren eines Schusses
         
        Parameter:      string Schussposition
                        object servereigene Spielerrepre�sentation
        R�ckgabewerte:  -
        """
        shot = str(clickedPos) + ";" + str(player)
        self.game.shoot(clickedPos, player)
        self.queue.put("s." + shot)
        
    def updatePlayerPosition(self, newPosition, player):
        """
        Updaten einer Position
         
        Parameter:      string Spielerposition
                        object servereigene Spielerrepre�sentation
        R�ckgabewerte:  -
        """
        index = self.players.index(player)
        self.playerPositions[index] = newPosition
  
        if self.queue.unfinished_tasks < 15:
            self.queue.put("p." + str(self.playerPositions))

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
        index = self.players.index(player)
        self.playerPositions[index] =  exitPoint        
        self.queue.put("r." + str(player) + str(room) + str(exitPoint))
        


##    def startGame(self):
##        """
##        Starten des Spiels
##         
##        Parameter:      -
##        R�ckgabewerte:  -
##        """
##        #for player in self.players:
##          #  self.sendToPlayer(player, 'GAMESTARTING')
##        self._gameStarted = True
##        t = threading.Thread(target = self.onTick)
##        t.daemon = True
##        t.start()
## 
##    def stopGame(self):
##        """
##        Stoppen des Spiels
##         
##        Parameter:      -
##        R�ckgabewerte:  -
##        """
##        self._gameStarted = False
        


