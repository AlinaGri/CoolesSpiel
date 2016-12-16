# -*- coding: cp1252 -*-
#Datum :    07-14.12.16
#Autor/en:  Alina, Lucas V.
#Version:   1.0

from entity import Entity
from weapon import Weapon
'''
Ein Player ist ein Objekt, das einen Namen/Erkennung (Nick), Position, Hp, Geschwindigkeit und eine Waffe hat.
er braucht eine Referenz zu einem game ueber den Server oder Client 
'''

class Player(Entity):
    def __init__(self, nick, rect = (0, 0, 3, 1), hitPoints = 20, speed = 1):
        '''
        Initialisation von Player
        Parameter:      rect
                            int mit der distanz nach links
                            int mit der disanz nach oben
                            int width von dem Objekt
                            int heigth von dem Objekt
                        Float Hitpoints vom Spieler
                        Float Bewegungsgeschwindigkeit vom Spieler
        return values:  -
        '''
        Entity.__init__(self, rect, speed)
        self.game = 0
        self.nick = nick
        self.hp = hitPoints
        self.weapon = self.secondaryWeapon()
    
    def shoot(self):
        '''
        Wenn moeglich (hoechstens wegen der zu vielen schussversuchen pro
        Sekunde nicht moeglich) wird ein Objekt Bullet erstellt.
        Falls keine Munition mehr vorhanden ist auf Standartwaffe wechseln
        Parameter:      -
        return values:  Boolean ODER None
                            je nachdem ob die Waffe einen schuss abfeuern darf
                            bsp. bei einer Waffengeschwindigkeit von 1 darf nach
                            0.5 Sekunden kein weiterer Schuss abgefeuert werden
        '''
        position = self.rect[0], self.rect[1]
        weapon = self.weapon
        bullet = weapon.createBullet(position)
        if weapon.ammo == 0:
            self.weapon = self.secondaryWeapon()
        return bullet
        
    def secondaryWeapon(self):
        '''
        Der Spieler bekommt das Objekt der Standartwaffe zugewiesen
        Parameter:      -
        return values:  -
        '''
        self.weapon = Weapon()
        
    def equipWeapon(self, weapon):
        '''
        Der Spieler bekommt ein Waffenobjekt
        Parameter:      Objekt aus einer Waffenklasse
        return values:  -
        '''
        self.weapon = weapon()

##################### Getters und Setters, die momentan nirgends gebraucht werden, aber dazu gehoeren #####################

    def getNick(self):
        '''
        Ausgabe des Spielernicknames
        Parameter:      -
        return values:  String, nickname des Spielers
        '''
        return self.nick
    
    def setNick(self, nick):
        '''
        setzt den Spielernickname
        Parameter:      String, nickname des Spielers
        return values:  -
        '''
        self.nick = nick
        
    def getHitpoints(self):
        '''
        Ausgabe der Spielerhitpoints
        Parameter:      -
        return values:  Float hitpoints des Spielers
        '''
        return self.hp
    
    def setHitpoints(self, hp):
        '''
        setzt die Spielerhitpoints
        Parameter:      Float, Spielerhitpoints
        return values:  -
        '''
        self.hp = hp
    
    def getWeapon(self):
        '''
        Ausgabe der Waffe des Spielers
        Parameter:      -
        return values:  Objekt, von einer der Klasse Weapon
        '''
        return self.weapon
    
    def setWeapon(self, weapon):
        '''
        Der Spieler bekommt ein Objekt der Klasse Weapon, auf self.weapon
        Parameter:      Objekt der Klasse Weapon
        return values:  -
        '''
        self.weapon = weapon
    