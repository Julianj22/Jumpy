from tkinter import *
from geometry import Bounds, Point2D
import sys

NoCollisionHexCodes = ["#00FF00", "#F0C080"]
OkCollisionHexCodes = ["#FFDF00", "#A8AAB1", "#FFFF00"]
P1InventoryList = []
P2InventoryList = []


def updateCollisionValue(hex):
    Agent.lastCollision = hex

class Agent:

    INTENSITIES = [4,5,6,7,8,7,6,5,4,3,2,1,0,1,2,3]

    def __init__(self,position,world):
        self.position = position
        self.world    = world
        self.world.add(self)
        self.ticks    = 0
        self.count = 0
        self.tempCords = None
        self.tempCords2 = None
        self.nonInteractableCords = None
        self.doorCords = None
        self.keyCords = None
        self.currentlyJumping = False
        self.lastCollision = None

    def color(self):
        a = self.ticks % len(self.INTENSITIES)
        return "#0000"+str(self.INTENSITIES[a])+"0"

    def shape(self):
        p1 = self.position + Vector2D( 0.125, 0.125)
        p2 = self.position + Vector2D(-0.125, 0.125)
        p3 = self.position + Vector2D(-0.125,-0.125)
        p4 = self.position + Vector2D( 0.125,-0.125)
        return [p1,p2,p3,p4]

    def filledspace(hex, list):
        # the input list should be a list of tuples which are coordinates
        dict = {}
        templist = []
        for tuple in list:
            templist.append(tuple)
            dict[hex] = templist
        return dict

    def collisionCheck(inputCord, inputDict):
        # base check if hex exists in which
        for hex in inputDict.keys():
            if hex in OkCollisionHexCodes:
                for hex in OkCollisionHexCodes:
                    counter = 0
                    listCounter = 0
                    checkCords = inputDict[hex]
                    while counter < len(checkCords):
                        if inputCord == checkCords[counter]:
                            updateCollisionValue(hex)
                            return True
                        counter += 1
                        listCounter += 1
                return False
            else:
                for hex in NoCollisionHexCodes:
                    counter = 0
                    listCounter = 0
                    checkCords = inputDict[hex]
                    while counter < len(checkCords):
                        if inputCord == checkCords[counter]:
                            return True
                        counter += 1
                        listCounter += 1
                return False

    def removeItemFromInventory(whichInv, item):
        if whichInv == 1 and item in P1InventoryList:
            P1InventoryList.remove(item)
        if whichInv == 2 and item in P2InventoryList:
            P2InventoryList.remove(item)

    def isInInventory(whichInv, item):
        if whichInv == 1:
            if item in P1InventoryList:
                return True
            else:
                return False
        if whichInv == 2:
            if item in P2InventoryList:
                return True
            else:
                return False

    def addItemtoInventory(whichInv, item):
        if whichInv == 1 and item not in P1InventoryList:
            P1InventoryList.append(item)
        if whichInv == 2 and item not in P2InventoryList:
            P2InventoryList.append(item)

    def update(self):
        self.ticks += 1

    def leave(self):
        self.world.remove(self)

class Game(Frame):

    # Game(name,w,h,ww,wh)
    #
    # Creates a world with a coordinate system of width w and heigh
    # h, with x coordinates ranging between -w/2 and w/2, and with y
    # coordinates ranging between -h/2 and h/2.
    #
    # Creates a corresponding graphics window, for rendering
    # the world, with pixel width ww and pixel height wh.
    #
    # The window will be named by the string given in name.
    #
    # The topology string is used by the 'trim' method to (maybe) keep
    # bodies within the frame of the world. (For example, 'wrapped'
    # yields "SPACEWAR" topology, i.e. a torus.)
    #
    def __init__(self, name, w, h, ww, wh, topology = 'wrapped', console_lines = 0):

        # Register the world coordinate and graphics parameters.
        self.WINDOW_WIDTH = ww
        self.WINDOW_HEIGHT = wh
        self.bounds = Bounds(-w/2,-h/2,w/2,h/2)
        self.topology = topology

        # Populate the world with creatures
        self.agents = []
        self.GAME_OVER = False
        self.GAME_WON = False

        # Initialize the graphics window.
        self.root = Tk()
        self.root.title(name)
        Frame.__init__(self, self.root)
        self.canvas = Canvas(self.root, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT)

        # Handle mouse pointer motion and keypress events.
        self.mouse_position = Point2D(0.0,0.0)
        self.mouse_down     = False
        self.bind_all('<Motion>',self.handle_mouse_motion)
        self.canvas.bind('<Button-1>',self.handle_mouse_press)
        self.canvas.bind('<ButtonRelease-1>',self.handle_mouse_release)
        self.bind_all('<Key>',self.handle_keypress)

        self.canvas.pack()
        if console_lines > 0:
            self.text = Text(self.root,height=console_lines,bg="#000000",fg="#A0F090",width=115)
            self.text.pack()
        else:
            self.text = None
        self.pack()

    def report(self,line=""):
        line += "\n"
        if self.text == None:
            print(line)
        else:
            self.text.insert(END,line)
            self.text.see(END)

    def trim(self,agent):
        if self.topology == 'wrapped':
            agent.position = self.bounds.wrap(agent.position)
        elif self.topology == 'bound':
            agent.position = self.bounds.clip(agent.position)
        elif self.topology == 'open':
            pass

    def add(self, agent):
        self.agents.append(agent)

    def remove(self, agent):
        self.agents.remove(agent)

    def update(self):
        for agent in self.agents:
            agent.update()
        self.clear()
        for agent in self.agents:
            self.draw_shape(agent.shape(),agent.color())
        Frame.update(self)
        if not self.GAME_WON:
            self.report("Move right: Player 1: 'd'  ~  Player 2: 'l'")
            self.report("Move left:  Player 1: 'a'  ~  Player 2: 'j'")
            self.report("Jump:       Player 1: 'w'  ~  Player 2: 'i'")
            self.report("Pause: 'Spacebar'")
            self.report("Quit: 'q'")
            if self.pause:
                self.report("Status: PAUSED")
            else:
                self.report("Status: NOT PAUSED")

            if not P1InventoryList:
                self.report("Player 1's inventory is empty.")
            else:
                inventoryString1 = ""
                itemCount1 = len(P1InventoryList)
                inventoryGrammar1 = ", "
                counter1 = 0
                for item in P1InventoryList:
                    inventoryString1 += str(item)
                    if counter1 < itemCount1 - 1:
                        inventoryString1 += inventoryGrammar1
                        counter1 += 1
                self.report("Player 1's inventory: {}".format(inventoryString1))

            if not P2InventoryList:
                self.report("Player 2's inventory is empty.")
            else:
                inventoryString2 = ""
                itemCount2 = len(P2InventoryList)
                inventoryGrammar2 = ", "
                counter2 = 0
                for item in P2InventoryList:
                    inventoryString2 += str(item)
                    if counter2 < itemCount2 - 1:
                        inventoryString2 += inventoryGrammar2
                        counter2 += 1
                self.report("Player 2's inventory: {}".format(inventoryString2))
        else:
            self.report("GAME OVER! YOU WON!")
            self.report("GAME OVER! YOU WON!")
            self.report("GAME OVER! YOU WON!")


    def draw_shape(self, shape, color):
        wh,ww = self.WINDOW_HEIGHT,self.WINDOW_WIDTH
        h = self.bounds.height()
        x = self.bounds.xmin
        y = self.bounds.ymin
        points = [ ((p.x - x)*wh/h, wh - (p.y - y)* wh/h) for p in shape ]
        first_point = points[0]
        points.append(first_point)
        self.canvas.create_polygon(points, fill=color)

    def clear(self):
        self.canvas.delete('all')
        self.canvas.create_rectangle(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, fill="#000000")

    def window_to_world(self,x,y):
        return self.bounds.point_at(x/self.WINDOW_WIDTH, 1.0-y/self.WINDOW_HEIGHT)

    def handle_mouse_motion(self,event):
        self.mouse_position = self.window_to_world(event.x,event.y)
        #print("MOUSE MOVED",self.mouse_position,self.mouse_down)

    def handle_mouse_press(self,event):
        self.mouse_down = True
        self.handle_mouse_motion(event)
        #print("MOUSE CLICKED",self.mouse_down)

    def handle_mouse_release(self,event):
        self.mouse_down = False
        self.handle_mouse_motion(event)
        #print("MOUSE RELEASED",self.mouse_down)

    def handle_keypress(self,event):
        if event.char == 'q':
            self.GAME_OVER = True
