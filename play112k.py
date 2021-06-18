from cmu_112_graphics import *
import random, string, math, time
from PIL import ImageTk, Image
import pygame

def almostEqual(d1, d2, epsilon=10**-7): #helper-fn
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# main app
#################################################
global name
name = ''

def distance2(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

class Cube(object):
    def __init__(self, coords, xAng, yAng, app):
        self.coords = coords
        self.xAng = xAng
        self.yAng = yAng
        self.floor = []
        for i in range(len(self.coords)):
            if self.coords[i][2] == 0:
                self.floor.append(i)
        self.leftWall = []
        for i in range(len(self.coords)):
            if self.coords[i][1] == 0:
                self.leftWall.append(i)
        self.rightWall = []
        for i in range(len(self.coords)):
            if self.coords[i][0] == 0:
                self.rightWall.append(i)
        self.translate2()
        self.translateTK(app)
        self.calculateSideLength()

    
    def calculateSideLength(self):
        maxLength = 0
        for coord1 in self.coords:
            for coord2 in self.coords: 
                if distance(coord1, coord2) > maxLength:
                    maxLength = distance(coord1, coord2)
        for coord1 in self.coords:
            for coord2 in self.coords: 
                if distance(coord1, coord2) < maxLength and distance(coord1, coord2) != 0:
                    self.sideLength = distance(coord1, coord2)


    def translate2(self):
        self.twoDCoords = []
        for coord in self.coords:
            x, y, z = coord
            twoX = math.cos(self.xAng)*x + math.cos(self.yAng)*y
            twoY = math.sin(self.xAng)*x + math.sin(self.yAng)*y + z
            twoCoord = (twoX, twoY)
            self.twoDCoords.append(twoCoord)
        
    def translateTK(self, app):
        self.tkCoords = []
        for coord in self.twoDCoords:
            x, y = coord
            newX = app.width/2+x
            newY = app.height/2-y+app.height/10
            self.tkCoords.append((newX, newY))

class Person(object):
    def __init__(self, center, xAng, yAng, app):
        self.center = center
        self.xAng = xAng
        self.yAng = yAng
        self.radiusX = 30
        self.radiusY = 40
        self.radiusZ = 10
        self.calculateCorners()
        self.translate2()
        self.translateTK(app)

    def calculateCorners(self):
        self.leftCorner = (self.center[0]+self.radiusX, self.center[1]-self.radiusY, self.center[2]-self.radiusZ)
        self.rightCorner = (self.center[0]-self.radiusX, self.center[1]+self.radiusY, self.center[2]+self.radiusZ)

    def translate2(self):
        # Center
        coord = self.center
        x, y, z = coord
        twoX = math.cos(self.xAng)*x + math.cos(self.yAng)*y
        twoY = math.sin(self.xAng)*x + math.sin(self.yAng)*y + z
        self.twoCoord = (twoX, twoY)

        # Left Corner
        coord = self.leftCorner
        x, y, z = coord
        twoX = math.cos(self.xAng)*x + math.cos(self.yAng)*y
        twoY = math.sin(self.xAng)*x + math.sin(self.yAng)*y + z
        self.leftCorner2d = (twoX, twoY)

        # Right Corner
        coord = self.rightCorner
        x, y, z = coord
        twoX = math.cos(self.xAng)*x + math.cos(self.yAng)*y
        twoY = math.sin(self.xAng)*x + math.sin(self.yAng)*y + z
        self.rightCorner2d = (twoX, twoY)
        
    def translateTK(self, app):
        x, y = self.twoCoord
        newX = app.width/2+x
        newY = app.height/2-y+app.height/10
        self.tkCoord = (newX, newY)
        
        x, y = self.leftCorner2d
        newX = app.width/2+x
        newY = app.height/2-y+app.height/10
        self.tkLeftCorner = (newX, newY)

        x, y = self.rightCorner2d
        newX = app.width/2+x
        newY = app.height/2-y+app.height/10
        self.tkRightCorner = (newX, newY)

class Ball(object):
    def __init__(self, center, xAng, yAng, radius, app):
        self.center = center
        self.xAng = xAng
        self.yAng = yAng
        self.radius = radius
        self.mass = 2
        self.netForce = -9.8*self.mass
        self.calculateCorners()
        self.translate2()
        self.translateTK(app)

    def calculateCorners(self):
        self.leftCorner = (self.center[0]+self.radius, self.center[1]-self.radius, self.center[2]-self.radius)
        self.rightCorner = (self.center[0]-self.radius, self.center[1]+self.radius, self.center[2]+self.radius)

    def translate2(self):
        # Center
        coord = self.center
        x, y, z = coord
        twoX = math.cos(self.xAng)*x + math.cos(self.yAng)*y
        twoY = math.sin(self.xAng)*x + math.sin(self.yAng)*y + z
        self.twoCoord = (twoX, twoY)

        # Left Corner
        coord = self.leftCorner
        x, y, z = coord
        twoX = math.cos(self.xAng)*x + math.cos(self.yAng)*y
        twoY = math.sin(self.xAng)*x + math.sin(self.yAng)*y + z
        self.leftCorner2d = (twoX, twoY)

        # Right Corner
        coord = self.rightCorner
        x, y, z = coord
        twoX = math.cos(self.xAng)*x + math.cos(self.yAng)*y
        twoY = math.sin(self.xAng)*x + math.sin(self.yAng)*y + z
        self.rightCorner2d = (twoX, twoY)
        
    def translateTK(self, app):
        x, y = self.twoCoord
        newX = app.width/2+x
        newY = app.height/2-y+app.height/10
        self.tkCoord = (newX, newY)
        
        x, y = self.leftCorner2d
        newX = app.width/2+x
        newY = app.height/2-y+app.height/10
        self.tkLeftCorner = (newX, newY)

        x, y = self.rightCorner2d
        newX = app.width/2+x
        newY = app.height/2-y+app.height/10
        self.tkRightCorner = (newX, newY)

    def changePosition(self, initVelocity, startingPosition, startTime, app):
        timeWarp = 3
        angle = app.ball.findAngleOfX(app)
        timePassed = time.time() - startTime
        cz = -9.8*(timeWarp*timePassed)**2 + timeWarp*initVelocity[2]*timePassed + startingPosition[2]
        velocityX = timeWarp*initVelocity[0]
        velocityY = timeWarp*initVelocity[1]
        cx = startingPosition[0] + velocityX*timePassed
        if startingPosition[1] - app.sideLength/2 <= 0:
            cy = startingPosition[1] - velocityY*timePassed
        else:
            cy = startingPosition[1] + velocityY*timePassed
        self.center = (cx, cy, cz)
        self.calculateCorners()
        self.translate2()
        self.translateTK(app)
        if (self.center[2] <= app.basket.center[2]):
            if ((abs(self.center[0] - (app.basket.center[0]-app.basket.radius)) < app.basket.radius*1.3) and 
                (abs(self.center[0] - (app.basket.center[0] + app.basket.radius)) < app.basket.radius*1.3) and
                (abs(self.center[1] - (app.basket.center[1]-app.basket.radius)) < app.basket.radius*1.3) and
                (abs(self.center[1] - (app.basket.center[1]-app.basket.radius)) < app.basket.radius*1.3)):
                app.bucket = True
                app.paused = True
                app.score += 1
                app.shots+=1
                app.timeShot = time.time()
                shootingPercent = round((app.score/app.shots)*100, 3) if app.shots!=0 else 0
                if shootingPercent > 65 and app.score > 2:
                    app.soundc.play()
                else:
                    app.sounda.play()
            else:
                app.brick = True
                app.paused = True
                app.shots+=1
                app.timeShot = time.time()
                app.soundb.play()
                
                
        if self.center[0] + self.radius < 0:
            app.paused = True
            app.brick = True
            app.shots+=1
            app.timeShot = time.time()
        self.checkPos(app)
        self.calculateCorners()
        self.translate2()
        self.translateTK(app)
    
    def checkPos(self, app):
        if self.center[0] < 0:
            self.center = (0, self.center[1], self.center[2])
        elif self.center[0] > app.sideLength:
            self.center = (app.sideLength, self.center[1], self.center[2])
        if self.center[1] < 0:
            self.center = (self.center[0], 0, self.center[2])
        elif self.center[1] > app.sideLength:
            self.center = (self.center[0], app.sideLength, self.center[2])
        if self.center[2] < 0:
            self.center = (self.center[0], self.center[1], 0)
        elif self.center[2] > app.sideLength:
            self.center = (self.center[0], self.center[1], app.sideLength)


    def findAngleOfX(self, app):
        dist = ((self.center[0]-app.basket.center[0])**2 + (self.center[1]-app.basket.center[1])**2)**0.5
        angle = math.asin(abs(self.center[1] - app.sideLength/2) / dist)
        return angle
    
    def findInitialVelocities(self, app):
        theta = app.ball.findAngleOfX(app)
        accuracyFactor = app.accuracy*(random.uniform(-1, 1))*app.basket.radius/(20)
        dist = ((self.center[0]-app.basket.center[0])**2 + (self.center[1]-app.basket.center[1])**2)**0.5 + accuracyFactor
        x = dist/2
        peakHeight = app.cube.sideLength*(1/2) + (1/4)*(dist)
        releaseAngle = math.atan((peakHeight - app.cube.sideLength*(1/2))/x)
        zVel = (9.8*dist)**0.5
        xVel = -((zVel/(math.tan(releaseAngle)))/2 + accuracyFactor)*math.cos(theta)
        yVel = -((zVel/(math.tan(releaseAngle)))/2 + accuracyFactor)*math.sin(theta)
        return (xVel, yVel, zVel)


class Basket(object):
    def __init__(self, center, xAng, yAng, radius, app):
        self.center = center
        self.xAng = xAng
        self.yAng = yAng
        self.radius = radius
        self.calculateCorners()
        self.translate2()
        self.translateTK(app)

    def calculateCorners(self):
        self.leftCorner = (self.center[0]+self.radius, self.center[1]-self.radius, self.center[2])
        self.rightCorner = (self.center[0]-self.radius, self.center[1]+self.radius, self.center[2])

    def translate2(self):
        # Center
        coord = self.center
        x, y, z = coord
        twoX = math.cos(self.xAng)*x + math.cos(self.yAng)*y
        twoY = math.sin(self.xAng)*x + math.sin(self.yAng)*y + z
        self.twoCoord = (twoX, twoY)

        # Left Corner
        coord = self.leftCorner
        x, y, z = coord
        twoX = math.cos(self.xAng)*x + math.cos(self.yAng)*y
        twoY = math.sin(self.xAng)*x + math.sin(self.yAng)*y + z
        self.leftCorner2d = (twoX, twoY)

        # Right Corner
        coord = self.rightCorner
        x, y, z = coord
        twoX = math.cos(self.xAng)*x + math.cos(self.yAng)*y
        twoY = math.sin(self.xAng)*x + math.sin(self.yAng)*y + z
        self.rightCorner2d = (twoX, twoY)
        
    def translateTK(self, app):
        x, y = self.twoCoord
        newX = app.width/2+x
        newY = app.height/2-y+app.height/10
        self.tkCoord = (newX, newY)
        
        x, y = self.leftCorner2d
        newX = app.width/2+x
        newY = app.height/2-y+app.height/10
        self.tkLeftCorner = (newX, newY)

        x, y = self.rightCorner2d
        newX = app.width/2+x
        newY = app.height/2-y+app.height/10
        self.tkRightCorner = (newX, newY)
    
def getImgs(app):
    app.stephenRun1 = app.loadImage("stephenRun1.png")
    app.stephenRun2 = app.loadImage("stephenRun2.png")
    app.stephenShoot = app.loadImage("stephenShoot.png")
    app.josiahRun1 = app.loadImage("josiahRun1.png")
    app.josiahRun2 = app.loadImage("josiahRun2.png")
    app.josiahShoot = app.loadImage("josiahShoot.png")
    app.seanRun1 = app.loadImage("seanRun1.png")
    app.seanRun2 = app.loadImage("seanRun2.png")
    app.seanShoot = app.loadImage("seanShoot.png")
    app.ottoRun1 = app.loadImage("ottoRun1.png")
    app.ottoRun2 = app.loadImage("ottoRun2.png")
    app.ottoShoot = app.loadImage("ottoShoot.png")
    app.stephenRun1 = app.stephenRun1.resize((60, 80))
    app.stephenRun2 = app.stephenRun2.resize((60, 80))
    app.stephenShoot = app.stephenShoot.resize((60, 80))
    app.stephenImgs = [app.stephenRun1, app.stephenRun2, app.stephenShoot]
    app.josiahRun1 = app.josiahRun1.resize((60, 80))
    app.josiahRun2 = app.josiahRun2.resize((60, 80))
    app.josiahShoot = app.josiahShoot.resize((60, 80))
    app.josiahImgs = [app.josiahRun1, app.josiahRun2, app.josiahShoot]
    app.seanRun1 = app.seanRun1.resize((60, 80))
    app.seanRun2 = app.seanRun2.resize((60, 80))
    app.seanShoot = app.seanShoot.resize((60, 80))
    app.seanImgs = [app.seanRun1, app.seanRun2, app.seanShoot]
    app.ottoRun1 = app.ottoRun1.resize((60, 80))
    app.ottoRun2 = app.ottoRun2.resize((60, 80))
    app.ottoShoot = app.ottoShoot.resize((60, 80))
    app.ottoImgs = [app.ottoRun1, app.ottoRun2, app.ottoShoot]
    app.playerImgs = [app.stephenImgs, app.josiahImgs, app.seanImgs, app.ottoImgs]

def appStarted(app):
    getImgs(app)
    appReset(app)
    app.startPlayerTime = time.time()
    pygame.init()
    pygame.mixer.init()
    app.sounda = pygame.mixer.Sound("sheesh.mp3")
    app.soundb = pygame.mixer.Sound("boo.mp3")
    app.soundc = pygame.mixer.Sound("superstar.mp3")
    
    
def appReset(app):
    app.playerName = play112k.name
    sizeChanged(app)
    app.initVelocity = (0, 0, 0)
    app.startingPosition = app.ball.center
    app.ballFired = False
    app.sliderValue = 0
    app.sliderTarget = random.randint(0,20)
    app.sliderIncreasing = True
    app.accuracy = 0
    app.brick = False
    app.bucket = False
    app.paused = False
    app.score = 0
    app.shots = 0
    app.timerDelay = 10
    app.rememberedAngle = None
    if app.playerName == "Stephen":
        app.player = 0
    elif app.playerName == "Josiah":
        app.player = 1
    elif app.playerName == "Sean":
        app.player = 2
    elif app.playerName == "Otto":
        app.player = 3
    app.pictureNumber = 0

def sizeChanged(app):
    app.sideLength = app.width/3.5
    sideLength = app.sideLength
    xAng = 7*math.pi/6
    yAng = 0
    app.person = Person((sideLength-sideLength/40, sideLength/2-10, sideLength/4), xAng, yAng, app)
    app.cube = Cube([(0,0,0), (0, sideLength, 0), (0, sideLength, sideLength), (sideLength, sideLength, sideLength), (sideLength, 0, 0), (sideLength, 0, sideLength), (0, 0, sideLength), (sideLength, sideLength, 0)], xAng, yAng, app)
    app.ball = Ball((sideLength-sideLength/40, sideLength/2, sideLength/4), xAng, yAng, sideLength/40, app)
    app.basket = Basket((sideLength/20, sideLength/2, sideLength/2), xAng, yAng, sideLength/20, app)

def mousePressed(app, event):
    if app.paused:
        return
    app.ball.center = (app.ball.center[0], app.ball.center[1], app.sideLength/2)
    print(app.startingPosition)
    app.startingPosition = app.ball.center
    print(app.startingPosition)
    app.accuracy = abs(app.sliderValue-app.sliderTarget)
    app.initVelocity = app.ball.findInitialVelocities(app)
    app.startTime = time.time()
    app.ballFired = True

def timerFired(app):
    app.pictureNumber = int((time.time() - app.startPlayerTime) % 2)
    if app.paused:
        if time.time() - app.timeShot > 1:
            resetBall(app)
        return
    if app.ballFired:
        app.ball.changePosition(app.initVelocity, app.startingPosition, app.startTime, app)
        app.pictureNumber = 2
    else:
        if app.sliderIncreasing:
            app.sliderValue += 1
        else:
            app.sliderValue -= 1
        if not (0 < app.sliderValue < 20):
            app.sliderIncreasing = not app.sliderIncreasing
    
    app.playerName = play112k.name

def resetBall(app):
    sizeChanged(app)
    app.initVelocity = (0, 0)
    app.startingPosition = app.ball.center
    app.ballFired = False
    app.sliderValue = 0
    app.sliderTarget = random.randint(0,20)
    app.sliderIncreasing = True
    app.accuracy = 0
    app.brick = False
    app.bucket = False
    app.paused = False
    app.rememberedAngle = None

def keyPressed(app, event):
    if event.key == "r":
        appReset(app)
    if event.key == "Enter":
        resetBall(app)
    if app.paused:
        return
    if event.key == "w":
        coords = app.ball.center
        newCoords = (coords[0]-10, coords[1], coords[2])
        app.ball.center = newCoords
        newCoords = (coords[0]-10, coords[1]-10, coords[2])
        app.person.center = newCoords
        app.ball.calculateCorners()
        app.ball.translate2()
        app.ball.translateTK(app)
        app.ball.checkPos(app)
        app.person.calculateCorners()
        app.person.translate2()
        app.person.translateTK(app)
    if event.key == "d":
        coords = app.ball.center
        newCoords = (coords[0], coords[1]+10, coords[2])
        app.ball.center = newCoords
        newCoords = (coords[0]-10, coords[1]-10, coords[2])
        app.person.center = newCoords
        app.ball.calculateCorners()
        app.ball.translate2()
        app.ball.translateTK(app)
        app.ball.checkPos(app)
        app.person.calculateCorners()
        app.person.translate2()
        app.person.translateTK(app)
    if event.key == "a":
        coords = app.ball.center
        newCoords = (coords[0], coords[1]-10, coords[2])
        app.ball.center = newCoords
        newCoords = (coords[0], coords[1]-20, coords[2])
        app.person.center = newCoords
        app.ball.calculateCorners()
        app.ball.translate2()
        app.ball.translateTK(app)
        app.ball.checkPos(app)
        app.person.calculateCorners()
        app.person.translate2()
        app.person.translateTK(app)
    if event.key == "s":
        coords = app.ball.center
        newCoords = (coords[0]+10, coords[1], coords[2])
        app.ball.center = newCoords
        newCoords = (coords[0]+10, coords[1]-10, coords[2])
        app.person.center = newCoords
        app.ball.calculateCorners()
        app.ball.translate2()
        app.ball.translateTK(app)
        app.ball.checkPos(app)
        app.person.calculateCorners()
        app.person.translate2()
        app.person.translateTK(app)

def distance(point1, point2):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    return ((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)**0.5


def redrawAll(app, canvas):
    canvas.create_polygon(app.cube.tkCoords[app.cube.floor[0]][0], app.cube.tkCoords[app.cube.floor[0]][1], app.cube.tkCoords[app.cube.floor[1]][0], app.cube.tkCoords[app.cube.floor[1]][1], app.cube.tkCoords[app.cube.floor[3]][0], app.cube.tkCoords[app.cube.floor[3]][1], app.cube.tkCoords[app.cube.floor[2]][0], app.cube.tkCoords[app.cube.floor[2]][1], fill = "#DC9550")
    canvas.create_polygon(app.cube.tkCoords[app.cube.leftWall[0]][0], app.cube.tkCoords[app.cube.leftWall[0]][1], app.cube.tkCoords[app.cube.leftWall[1]][0], app.cube.tkCoords[app.cube.leftWall[1]][1], app.cube.tkCoords[app.cube.leftWall[2]][0], app.cube.tkCoords[app.cube.leftWall[2]][1], app.cube.tkCoords[app.cube.leftWall[3]][0], app.cube.tkCoords[app.cube.leftWall[3]][1], fill = "#975B26")
    canvas.create_polygon(app.cube.tkCoords[app.cube.rightWall[0]][0], app.cube.tkCoords[app.cube.rightWall[0]][1], app.cube.tkCoords[app.cube.rightWall[1]][0], app.cube.tkCoords[app.cube.rightWall[1]][1], app.cube.tkCoords[app.cube.rightWall[2]][0], app.cube.tkCoords[app.cube.rightWall[2]][1], app.cube.tkCoords[app.cube.rightWall[3]][0], app.cube.tkCoords[app.cube.rightWall[3]][1], fill = "#703210")
    bottomCorner = app.cube.tkCoords[app.cube.rightWall[0]]
    rightCorner = app.cube.tkCoords[app.cube.rightWall[3]]
    midPt = (bottomCorner[0] + rightCorner[0])/2
    canvas.create_rectangle(bottomCorner[0]+app.sideLength/2-5, bottomCorner[1], bottomCorner[0]+app.sideLength/2+5, bottomCorner[1]-app.sideLength/2, fill="#C0C0C0", width=0)
    canvas.create_rectangle(bottomCorner[0]+app.sideLength/2-35, bottomCorner[1]-app.sideLength/2, bottomCorner[0]+app.sideLength/2+35, bottomCorner[1]-app.sideLength/2-40, fill="white", width=0)
    canvas.create_rectangle(bottomCorner[0]+app.sideLength/2-15, bottomCorner[1]-app.sideLength/2, bottomCorner[0]+app.sideLength/2+15, bottomCorner[1]-app.sideLength/2-20, fill="white", width=2, outline="orange")
    canvas.create_image(app.person.tkCoord[0], app.person.tkCoord[1], image=ImageTk.PhotoImage(app.playerImgs[app.player][app.pictureNumber]))
    canvas.create_oval(app.ball.tkLeftCorner[0], app.ball.tkLeftCorner[1], app.ball.tkRightCorner[0], app.ball.tkRightCorner[1], fill="orange")
    canvas.create_oval(app.basket.tkLeftCorner[0], app.basket.tkLeftCorner[1], app.basket.tkRightCorner[0], app.basket.tkRightCorner[1], outline = "#E45317" , width = 3)
    sliderLength = 100
    sliderStep = sliderLength/20
    canvas.create_rectangle(50, 50, sliderLength+50, 70)
    canvas.create_rectangle(50 + app.sliderTarget*sliderStep-10, 50, 50 + app.sliderTarget*sliderStep+10, 70, fill="green")
    canvas.create_rectangle(app.sliderValue*sliderStep - 5 + 50, 30, app.sliderValue*sliderStep + 5 + 50, 90, fill="black")
    if app.bucket:
        canvas.create_text(app.width/2, app.height/2, fill="green", text="SHIII! THATS A BUCKET", font="Arial 40 bold")
    if app.brick:
        canvas.create_text(app.width/2, app.height/2, fill="red", text="BRICK!", font="Arial 40 bold")
    scoreText = "Score: "+str(app.score)
    canvas.create_text(app.width*(3/4), app.height*(3/4), fill="black", text=scoreText, font="Arial 20 bold")
    shootingPercent = round((app.score/app.shots)*100, 3) if app.shots!=0 else 0
    percentText = "Shooting %: "+str(shootingPercent)
    canvas.create_text(app.width*(3/4), app.height*(3/4)+20, fill="black", text=percentText, font="Arial 20 bold")
    canvas.create_text(app.width * 5/6, app.height * 1/6, text = f'Player: {app.playerName}', font = "Arial 20 bold")



def play112k():
    runApp(width = 650, height = 550)