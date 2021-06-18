from play112k import *
from cmu_112_graphics import *
import pyautogui

def appStarted(app):
    app.stephenFill = "white"
    app.seanFill = "white"
    app.ottoFill = "white"
    app.josiahFill = "white"
    app.margin = 50
    app.player = None

    #load images
    app.stephenImg = app.loadImage("stephen.jpg")
    app.seanImg = app.loadImage("sean.jpg")
    app.ottoImg = app.loadImage("otto.jpg")
    app.josiahImg = app.loadImage("josiah.jpg")
    
    #resize images
    distance = (app.width // 2) - 2*app.margin - 25
    app.stephenImg = app.stephenImg.resize((distance,distance))
    app.seanImg = app.seanImg.resize((distance,distance))
    app.ottoImg = app.ottoImg.resize((distance,distance))
    app.josiahImg = app.josiahImg.resize((distance,distance))

def timerFired(app):
    checkHover(app)

def mousePressed(app, event):
    x = event.x
    y = event.y
    #play game if chosed a chacters
    stephenX0 = app.margin
    stephenY0 = app.margin
    stephenX1 = (app.width // 2) - app.margin
    stephenY1 = (app.height // 2) - app.margin
    if (stephenX0 <= x <= stephenX1) and (stephenY0 <= y <= stephenY1):
        play112k.name = "Stephen"
        play112k()
        
        

    seanX0 = (app.width // 2) + app.margin
    seanY0 = app.margin
    seanX1 = app.width - app.margin
    seanY1 = (app.height // 2) - app.margin
    if (seanX0 <= x <= seanX1) and (seanY0 <= y <= seanY1):
        play112k.name = "Sean"
        play112k()


    ottoX0 = app.margin
    ottoY0 = (app.height // 2) + app.margin
    ottoX1 = (app.width // 2) - app.margin
    ottoY1 = app.height - app.margin
    if (ottoX0 <= x <= ottoX1) and (ottoY0 <= y <= ottoY1):
        play112k.name = "Otto"
        play112k()


    josiahX0 = (app.width // 2) + app.margin
    josiahY0 = (app.height // 2) + app.margin
    josiahX1 = app.width - app.margin
    josiahY1 = app.height - app.margin
    if (josiahX0 <= x <= josiahX1) and (josiahY0 <= y <= josiahY1):
        play112k.name = "Josiah"
        play112k()

def checkHover(app):
    (x , y) = pyautogui.position()
    x -= 10
    y -= 45

    stephenX0 = app.margin
    stephenY0 = app.margin
    stephenX1 = (app.width // 2) - app.margin
    stephenY1 = (app.height // 2) - app.margin
    if (stephenX0 <= x <= stephenX1) and (stephenY0 <= y <= stephenY1):
        app.stephenFill = "red"
    else:
        app.stephenFill = "white"

    seanX0 = (app.width // 2) + app.margin
    seanY0 = app.margin
    seanX1 = app.width - app.margin
    seanY1 = (app.height // 2) - app.margin
    if (seanX0 <= x <= seanX1) and (seanY0 <= y <= seanY1):
        app.seanFill = "red"
    else:
        app.seanFill = "white"

    ottoX0 = app.margin
    ottoY0 = (app.height // 2) + app.margin
    ottoX1 = (app.width // 2) - app.margin
    ottoY1 = app.height - app.margin
    if (ottoX0 <= x <= ottoX1) and (ottoY0 <= y <= ottoY1):
        app.ottoFill = "red"
    else:
        app.ottoFill = "white"

    josiahX0 = (app.width // 2) + app.margin
    josiahY0 = (app.height // 2) + app.margin
    josiahX1 = app.width - app.margin
    josiahY1 = app.height - app.margin
    if (josiahX0 <= x <= josiahX1) and (josiahY0 <= y <= josiahY1):
        app.josiahFill = "red"
    else:
        app.josiahFill = "white"


    
def redrawAll(app, canvas):
    drawStephenChar(app, canvas)
    drawSeanChar(app, canvas)
    drawOttoChar(app, canvas)
    drawJosiah(app, canvas)
    drawInstructions(app, canvas)

def drawInstructions(app, canvas):
    canvas.create_text(app.width // 2, app.height // 2,
                        text = "Choose Your Character!",
                        font = "Arial 20 bold")

def drawStephenChar(app, canvas):
    #draw tab outlines top left
    x0 = app.margin
    y0 = app.margin
    x1 = (app.width // 2) - app.margin
    y1 = (app.height // 2) - app.margin
    canvas.create_rectangle(x0, y0, x1, y1, width = 2, fill = app.stephenFill)

    #picture
    picX = (x0 + x1) // 2
    picY = (y0 + y1) // 2
    canvas.create_image(picX, picY, image= ImageTk.PhotoImage(app.stephenImg))

def drawSeanChar(app, canvas):
    #draw tab outlines top right
    x0 = (app.width // 2) + app.margin
    y0 = app.margin
    x1 = app.width - app.margin
    y1 = (app.height // 2) - app.margin
    canvas.create_rectangle(x0, y0, x1, y1, width = 2, fill = app.seanFill)

    #picture
    picX = (x0 + x1) // 2
    picY = (y0 + y1) // 2
    canvas.create_image(picX, picY, image= ImageTk.PhotoImage(app.seanImg))

def drawOttoChar(app, canvas):
    #draw tab outlines bottom left
    x0 = app.margin
    y0 = (app.height // 2) + app.margin
    x1 = (app.width // 2) - app.margin
    y1 = app.height - app.margin
    canvas.create_rectangle(x0, y0, x1, y1, width = 2, fill = app.ottoFill)

    #picture
    picX = (x0 + x1) // 2
    picY = (y0 + y1) // 2
    canvas.create_image(picX, picY, image= ImageTk.PhotoImage(app.ottoImg))

def drawJosiah(app, canvas):
    #draw tab outlines bottom right
    x0 = (app.width // 2) + app.margin
    y0 = (app.height // 2) + app.margin
    x1 = app.width - app.margin
    y1 = app.height - app.margin
    canvas.create_rectangle(x0, y0, x1, y1, width = 2, fill = app.josiahFill)
    
    #picture
    picX = (x0 + x1) // 2
    picY = (y0 + y1) // 2
    canvas.create_image(picX, picY, image= ImageTk.PhotoImage(app.josiahImg))

def selectChar():
    runApp(width=750, height=750)
