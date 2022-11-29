from tkinter import *
from Game import Game, Agent
from geometry import Point2D, Vector2D
import math
import random
import time
from time import sleep

# saving cordinates for floor
FloorCordsList = []
FloorXCounter = 0
FloorXcord = -30.1
FloorYcord = -20.4
FloorYCounter = 0
while FloorYCounter <= 10:
    FloorYcord -= 0.1
    FloorXCounter = 0
    FloorYCounter += 1
    FloorXcord = -30.1
    while FloorXCounter <= 600:
        FloorXcord += 0.1
        FloorXcord, FloorYcord = round(FloorXcord, 3), round(FloorYcord, 3)
        FloorCordsList.append((FloorXcord, FloorYcord))
        FloorXCounter += 1
Agent.tempCords = Agent.filledspace("#00FF00", FloorCordsList)


# djc = double jump coin
# saving cords for djc
djcCordsList = []
djcXCounter = 0
djcXcord = -6.1
djcYcord = -9.9
djcYCounter = 0
while djcYCounter <= 10:
    djcYcord -= 0.1
    djcXCounter = 0
    djcYCounter += 1
    djcXcord = -6.1
    while djcXCounter <= 10:
        djcXcord += 0.1
        djcXcord, djcYcord = round(djcXcord, 3), round(djcYcord, 3)
        djcCordsList.append((djcXcord, djcYcord))
        djcXCounter += 1

# saving cords for key
keyCordsList = []
keyXCounter = 0
keyXcord = 16.4
keyYcord = -1.4
keyYCounter = 0
while keyYCounter <= 20:
    keyYcord -= 0.1
    keyXCounter = 0
    keyYCounter += 1
    keyXcord = 16.4
    while keyXCounter <= 10:
        keyXcord += 0.1
        keyXcord, keyYcord = round(keyXcord, 3), round(keyYcord, 3)
        keyCordsList.append((keyXcord,keyYcord))
        keyXCounter += 1

# saving cords for door
doorCordsList = []
doorXCounter = 0
doorXcord = 5.9
doorYcord = 12.9
doorYCounter = 0
while doorYCounter <= 60:
    doorYcord -= 0.1
    doorXCounter = 0
    doorYCounter += 1
    doorXcord = 5.9
    while doorXCounter <= 20:
        doorXcord += 0.1
        doorXcord, doorYcord = round(doorXcord, 3), round(doorYcord, 3)
        doorCordsList.append((doorXcord,doorYcord))
        doorXCounter += 1

class JGame(Game):

    def __init__(self):
        Game.__init__(self, 'Jumpy', 60.0, 45.0, 800, 600, topology='bound', console_lines=9)
        self.jumpCount=0
        self.pauseCount=0
        self.pause=False
        for plat in plats:
            self.platform = Platform(Point2D(plat[0],plat[1]),self)
        self.floor = Floor(Point2D(0,-22), self)
        self.player1 = Player1(Point2D(-25,-20.5), self)
        self.player2 = Player2(Point2D(25,-20.5), self)
        self.door = Door(Point2D(7,12.5),self)
        self.key = Key(Point2D(17,-2),self)
        self.coinCheck1 = False
        self.coinCheck2 = False
        self.keyCheck1 = False
        self.keyCheck2 = False
        self.doorCheck1 = False
        self.doorCheck2 = False
        self.winCheck1 = False
        self.winCheck2 = False
        self.DoubleJumpCoin = DoubleJumpCoin(Point2D(-5.5,-10.5), self)

    def handle_keypress(self,event):
        Game.handle_keypress(self,event)
        if event.char == 'w' and self.pause== False:
            if not Agent.collisionCheck((game.player1.position.x, game.player1.position.y), Agent.nonInteractableCords)==False:
                self.player1.jump_up()
                self.jumpCount=0
            elif self.jumpCount<2 and self.coinCheck1:
                self.player1.jump_up()
            self.jumpCount+=1

        elif event.char == "a"  and self.pause== False:
            self.player1.move_left()

        elif event.char == "d"  and self.pause== False:
            self.player1.move_right()

        elif event.char == 'i'  and self.pause== False:
            if not Agent.collisionCheck((game.player2.position.x, game.player2.position.y), Agent.nonInteractableCords)==False:
                self.player2.jump_up()
                self.jumpCount=0
            elif self.jumpCount<2 and self.coinCheck2:
                self.player2.jump_up()
            self.jumpCount+=1

        elif event.char == "j"  and self.pause== False:
            self.player2.move_left()

        elif event.char == "l"  and self.pause== False:
            self.player2.move_right()

        elif event.char == " ":
            self.pauseCount+=1
            if self.pauseCount%2!=0:
                self.pause = True
            else:
                self.pause = False

class Platform(Agent):

    def color(self):
        return "#F0C080"

    def shape(self):
        p1 = self.position + Vector2D( 5, 0.5)
        p2 = self.position + Vector2D(-5, 0.5)
        p3 = self.position + Vector2D(-5,-0.5)
        p4 = self.position + Vector2D( 5,-0.5)
        return [p1,p2,p3,p4]

# setting up platform cordinates #
plats = [[-15,-20], [-5,-12], [-20, -5], [-3, 0], [5, 10], [15,20], [16,-4]]
PlatsCordsList = []
for eachPlatform in plats:
    PlatYcord = eachPlatform[1] + 1.6
    PlatXcord = eachPlatform[0] - 5.1
    PlatXCounter = 0
    PlatYCounter = 0
    while PlatYCounter <= 10:
        PlatYcord -= 0.1
        PlatXCounter = 0
        PlatYCounter += 1
        PlatXcord = eachPlatform[0] - 5.1
        while PlatXCounter <= 100:
            PlatXcord += 0.1
            PlatXcord, PlatYcord = round(PlatXcord, 3), round(PlatYcord, 3)
            PlatsCordsList.append((PlatXcord, PlatYcord))
            PlatXCounter += 1
# setting up platform cordinates #

# formatting the data into a format accepted by the collision checking method #
Agent.tempCords2 = Agent.filledspace("#F0C080", PlatsCordsList)
Agent.nonInteractableCords = Agent.tempCords2 | Agent.tempCords
Agent.tempCords, Agent.tempCords2 = None, None
Agent.interactableCords = Agent.filledspace("#FFDF00", djcCordsList)
Agent.keyCords = Agent.filledspace("#A8AAB1", keyCordsList)
Agent.interactableCords = Agent.interactableCords | Agent.keyCords
Agent.doorCords = Agent.filledspace("#FFFF00", doorCordsList)
Agent.interactableCords = Agent.interactableCords | Agent.doorCords
# formatting the data into a format accepted by the collision checking method #


class Player1(Agent):
# with moving, it checks all the directions for collision, then moves
    def color(self):
        return "#00FFFF"

    def shape(self):
        p1 = self.position + Vector2D( 1, 1)
        p2 = self.position + Vector2D(-1, 1)
        p3 = self.position + Vector2D(-1,-1)
        p4 = self.position + Vector2D( 1,-1)
        return [p1,p2,p3,p4]

    def move_down(self):
        if not Agent.collisionCheck((self.position.x, self.position.y), Agent.nonInteractableCords):
            if Agent.collisionCheck((self.position.x, self.position.y), Agent.interactableCords):
                if Agent.lastCollision == "#A8AAB1":
                    game.keyCheck1 = True
                    Agent.addItemtoInventory(1,"Door Key")
                if Agent.lastCollision == "#FFDF00":
                    game.coinCheck1 = True
                    Agent.addItemtoInventory(1,"Double Jump Coin")
                if Agent.lastCollision == "#FFFF00":
                    game.doorCheck1 = True
                    if Agent.isInInventory(1, "Door Key"):
                        game.winCheck1 = True
                        game.remove(self)
                    Agent.removeItemFromInventory(1,"Door Key")
            self.position.y -= 0.5

    def move_up(self):
        if not Agent.collisionCheck((self.position.x, self.position.y + 2), Agent.nonInteractableCords):
            if Agent.collisionCheck((self.position.x, self.position.y + 2), Agent.interactableCords):
                if Agent.lastCollision == "#A8AAB1":
                    game.keyCheck1 = True
                    Agent.addItemtoInventory(1,"Door Key")
                if Agent.lastCollision == "#FFDF00":
                    game.coinCheck1 = True
                    Agent.addItemtoInventory(1,"Double Jump Coin")
                if Agent.lastCollision == "#FFFF00":
                    game.doorCheck1 = True
                    if Agent.isInInventory(1, "Door Key"):
                        game.winCheck1 = True
                        game.remove(self)
                    Agent.removeItemFromInventory(1,"Door Key")
            self.position.y += 1

    def move_left(self):
        if not Agent.collisionCheck((self.position.x - 1, self.position.y + 0.5), Agent.nonInteractableCords):
            if not Agent.collisionCheck((self.position.x - 1, self.position.y + 1), Agent.nonInteractableCords):
                if Agent.collisionCheck((self.position.x - 1, self.position.y), Agent.interactableCords):
                    if Agent.collisionCheck((self.position.x - 1, self.position.y), Agent.interactableCords):
                        if Agent.lastCollision == "#A8AAB1":
                            game.keyCheck1 = True
                            Agent.addItemtoInventory(1,"Door Key")
                        if Agent.lastCollision == "#FFDF00":
                            game.coinCheck1 = True
                            Agent.addItemtoInventory(1,"Double Jump Coin")
                        if Agent.lastCollision == "#FFFF00":
                            game.doorCheck1 = True
                            if Agent.isInInventory(1, "Door Key"):
                                game.winCheck1 = True
                                game.remove(self)
                            Agent.removeItemFromInventory(1,"Door Key")
                self.position.x -= 1

    def move_right(self):
        if not Agent.collisionCheck((self.position.x + 1, self.position.y + 0.5), Agent.nonInteractableCords):
            if not Agent.collisionCheck((self.position.x + 1, self.position.y + 1), Agent.nonInteractableCords):
                if Agent.collisionCheck((self.position.x + 1, self.position.y), Agent.interactableCords):
                    if Agent.collisionCheck((self.position.x + 1, self.position.y), Agent.interactableCords):
                        if Agent.lastCollision == "#A8AAB1":
                            game.keyCheck1 = True
                            Agent.addItemtoInventory(1,"Door Key")
                        if Agent.lastCollision == "#FFDF00":
                            game.coinCheck1 = True
                            Agent.addItemtoInventory(1,"Double Jump Coin")
                        if Agent.lastCollision == "#FFFF00":
                            game.doorCheck1 = True
                            if Agent.isInInventory(1, "Door Key"):
                                game.winCheck1 = True
                                game.remove(self)
                            Agent.removeItemFromInventory(1,"Door Key")
                self.position.x += 1

    def jump_up(self):
        self.currentlyJumping = True
        counter = 0
        while counter <= 10:
            self.move_up()
            counter += 1
        self.currentlyJumping = False

    def update(self):
        if game.pause == False and self.currentlyJumping is False:
            if self.position.y > -20.5:
                self.move_down()

class Player2(Agent):
# with moving, it checks all the directions for collision, then moves
    def color(self):
        return "#FFC0CB"

    def shape(self):
        p1 = self.position + Vector2D( 1, 1)
        p2 = self.position + Vector2D(-1, 1)
        p3 = self.position + Vector2D(-1,-1)
        p4 = self.position + Vector2D( 1,-1)
        return [p1,p2,p3,p4]

    def move_down(self):
        if not Agent.collisionCheck((self.position.x, self.position.y), Agent.nonInteractableCords):
            if Agent.collisionCheck((self.position.x, self.position.y), Agent.interactableCords):
                if Agent.lastCollision == "#A8AAB1":
                    game.keyCheck2 = True
                    Agent.addItemtoInventory(2,"Door Key")
                if Agent.lastCollision == "#FFDF00":
                    game.coinCheck2 = True
                    Agent.addItemtoInventory(2,"Double Jump Coin")
                if Agent.lastCollision == "#FFFF00":
                    game.doorCheck2 = True
                    if Agent.isInInventory(2, "Door Key"):
                        game.winCheck2 = True
                        game.remove(self)
                    Agent.removeItemFromInventory(2,"Door Key")
            self.position.y -= 0.5

    def move_up(self):
        if not Agent.collisionCheck((self.position.x, self.position.y + 2), Agent.nonInteractableCords):
            if Agent.collisionCheck((self.position.x, self.position.y + 2), Agent.interactableCords):
                if Agent.lastCollision == "#A8AAB1":
                    game.keyCheck2 = True
                    Agent.addItemtoInventory(2,"Door Key")
                if Agent.lastCollision == "#FFDF00":
                    game.coinCheck2 = True
                    Agent.addItemtoInventory(2,"Double Jump Coin")
                if Agent.lastCollision == "#FFFF00":
                    game.doorCheck2 = True
                    if Agent.isInInventory(2, "Door Key"):
                        game.winCheck2 = True
                        game.remove(self)
                    Agent.removeItemFromInventory(2,"Door Key")
            self.position.y += 1

    def move_left(self):
        if not Agent.collisionCheck((self.position.x - 1, self.position.y + 0.5), Agent.nonInteractableCords):
            if not Agent.collisionCheck((self.position.x - 1, self.position.y + 1), Agent.nonInteractableCords):
                if Agent.collisionCheck((self.position.x - 1, self.position.y), Agent.interactableCords):
                    if Agent.collisionCheck((self.position.x - 1, self.position.y), Agent.interactableCords):
                        if Agent.lastCollision == "#A8AAB1":
                            game.keyCheck2 = True
                            Agent.addItemtoInventory(2,"Door Key")
                        if Agent.lastCollision == "#FFDF00":
                            game.coinCheck2 = True
                            Agent.addItemtoInventory(2,"Double Jump Coin")
                        if Agent.lastCollision == "#FFFF00":
                            game.doorCheck2 = True
                            if Agent.isInInventory(2, "Door Key"):
                                game.winCheck2 = True
                                game.remove(self)
                            Agent.removeItemFromInventory(2,"Door Key")
                self.position.x -= 1

    def move_right(self):
        if not Agent.collisionCheck((self.position.x + 1, self.position.y + 0.5), Agent.nonInteractableCords):
            if not Agent.collisionCheck((self.position.x + 1, self.position.y + 1), Agent.nonInteractableCords):
                if Agent.collisionCheck((self.position.x + 1, self.position.y), Agent.interactableCords):
                    if Agent.collisionCheck((self.position.x + 1, self.position.y), Agent.interactableCords):
                        if Agent.lastCollision == "#A8AAB1":
                            game.keyCheck2 = True
                            Agent.addItemtoInventory(2,"Door Key")
                        if Agent.lastCollision == "#FFDF00":
                            game.coinCheck2 = True
                            Agent.addItemtoInventory(2,"Double Jump Coin")
                        if Agent.lastCollision == "#FFFF00":
                            game.doorCheck2 = True
                            if Agent.isInInventory(2, "Door Key"):
                                game.winCheck2 = True
                                game.remove(self)
                            Agent.removeItemFromInventory(2,"Door Key")
                self.position.x += 1

    def jump_up(self):
        self.currentlyJumping = True
        counter = 0
        while counter <= 10:
            self.move_up()
            counter += 1
        self.currentlyJumping = False

    def update(self):
        if game.pause == False and self.currentlyJumping is False:
            if self.position.y > -20.5:
                self.move_down()

class Door(Agent):

    def color(self):
        return "#FFFF00"

    def shape(self):
        p1 = self.position + Vector2D( 1, 2)
        p2 = self.position + Vector2D(-1, 2)
        p3 = self.position + Vector2D(-1,-2)
        p4 = self.position + Vector2D( 1,-2)
        return [p1,p2,p3,p4]

    def update(self):
        if game.winCheck1 and game.winCheck2:
            game.GAME_WON = True

class DoubleJumpCoin(Agent):

    def __init__(self,position, world):
        super().__init__(position, world)

    def color(self):
        return "#FFDF00"

    def shape(self):
        p1 = self.position + Vector2D( 0.5, 0.5)
        p2 = self.position + Vector2D(-0.5, 0.5)
        p3 = self.position + Vector2D(-0.5,-0.5)
        p4 = self.position + Vector2D( 0.5,-0.5)
        return [p1,p2,p3,p4]

    def update(self):
        if game.coinCheck1 and game.coinCheck2:
            game.remove(self)

class Floor(Agent):

    def color(self):
        return "#00FF00"

    def shape(self):
        p1 = self.position + Vector2D(40, .5)
        p2 = self.position + Vector2D(-40, 0.5)
        p3 = self.position + Vector2D(-40,-0.5)
        p4 = self.position + Vector2D( 40,-0.5)
        return [p1,p2,p3,p4]

class Key(Agent):

    def color(self):
        return "#A8AAB1"

    def shape(self):
        p1 = self.position + Vector2D( 0.5, 1)
        p2 = self.position + Vector2D(-0.5, 1)
        p3 = self.position + Vector2D(-0.5,-1)
        p4 = self.position + Vector2D( 0.5,-1)
        return [p1,p2,p3,p4]

    def update(self):
        if game.keyCheck1 and game.keyCheck2:
            game.remove(self)

print("WELCOME TO JUMPY")
game = JGame()
while not game.GAME_OVER:
    time.sleep(1.0/60.0)
    game.update()
