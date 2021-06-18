from play112k import *
from cmu_112_graphics import *
import pyautogui
from char_select import*

class HelpMode(Mode):
    def appStarted(mode):
        mode.backFill = "grey"

    def mousePressed(mode, event):
        x = event.x
        y = event.y
        backTab = ((mode.width /  2) + 1/10* mode.width, 
                        (mode.height / 2) + 3/10* mode.height, 
                        (mode.width / 2) + 4/10* mode.width,
                        (mode.height /  2) + 4/10* mode.height)
        backX0, backY0, backX1, backY1 = backTab
        if (backX0 <= x <= backX1) and (backY0 <= y <= backY1):
            mode.app.setActiveMode(mode.app.menuMode)

    def checkHover(mode):
        (x ,y) = pyautogui.position()
        x -= 10
        y -= 45
        backTab = ((mode.width /  2) + 1/10* mode.width, 
                        (mode.height / 2) + 3/10* mode.height, 
                        (mode.width / 2) + 4/10* mode.width,
                        (mode.height /  2) + 4/10* mode.height)
        backX0, backY0, backX1, backY1 = backTab
        if (backX0 <= x <= backX1) and (backY0 <= y <= backY1):
            mode.backFill = "red"
        else:
            mode.backFill = None

    def timerFired(mode):
        mode.checkHover()
        
    def redrawAll(mode, canvas):
        mode.drawText(canvas)
        mode.drawBackTab(canvas)

    def drawText(mode, canvas):
        canvas.create_text(mode.width // 2, mode.height * 1/10, 
                            text = "Welcome to NBA 112K!",
                            font = "Arial 20 bold")

        text = ["Directions:", "Time your click the best you can to"," try and make the ball into the basket!",
                "Use the arrow keys to move","the ball around in our 3D enviroment."]

        for i in range(len(text)):
            canvas.create_text(mode.width // 2, mode.height * (2 + i)/ 10,
                                text = text[i], font = "Arial 11 bold")

    def drawBackTab(mode, canvas):
        backTab = ((mode.width /  2) + 1/10* mode.width, 
                        (mode.height / 2) + 3/10* mode.height, 
                        (mode.width / 2) + 4/10* mode.width,
                        (mode.height /  2) + 4/10* mode.height)
        backX0, backY0, backX1, backY1 = backTab
        canvas.create_rectangle(backX0, backY0, backX1, backY1, fill = mode.backFill)
        canvas.create_text((backX0 + backX1) // 2, (backY0 + backY1) // 2, text = "Back",
                            font = "Arial 12 bold")

   
class MenuMode(Mode):
    def appStarted(mode):
        mode.playFill = "white"
        mode.helpFill = "white"

    def mousePressed(mode, event):
        x = event.x
        y = event.y
        #play game if click on play
        playTab = ((mode.width /  2) - 1/4* mode.width, 
                        (mode.height / 2.5) - 1/12* mode.height, 
                        (mode.width / 2) + 1/4* mode.width,
                        (mode.height /  2.5) + 1/12* mode.height)
        playX0, playY0, playX1, playY1 = playTab
        if (playX0 <= x <= playX1) and (playY0 <= y <= playY1):
            selectChar()
            

        #get help if clicked on help
        helpTab = ((mode.width // 2) - 1/4* mode.width, 
                        (mode.height // 1.65) - 1/12* mode.height, 
                        (mode.width // 2) + 1/4* mode.width,
                        (mode.height // 1.65) + 1/12* mode.height)
        helpX0, helpY0, helpX1, helpY1 = helpTab
        if (helpX0 <= x <= helpX1) and (helpY0 <= y <= helpY1):
            mode.app.setActiveMode(mode.app.helpMode)


    def checkHover(mode):
        #http://www.learningaboutelectronics.com/Articles/How-to-get-the-current-position-of-mouse-in-Python-using-pyautogui.php#:~:text=To%20determine%20the%20mouse's%20current,where%20the%20mouse%20cursor%20is.
        
        
        (x ,y) = pyautogui.position()
        x -= 10
        y -= 45

        #check hover position for playTab
        playTab = ((mode.width /  2) - 1/4* mode.width, 
                        (mode.height / 2.5) - 1/12* mode.height, 
                        (mode.width / 2) + 1/4* mode.width,
                        (mode.height /  2.5) + 1/12* mode.height)
        playX0, playY0, playX1, playY1 = playTab
        if (playX0 <= x <= playX1) and (playY0 <= y <= playY1):
            mode.playFill = "red"
        else:
            mode.playFill = "white"

        #check hover position for helpTab
        helpTab = ((mode.width // 2) - 1/4* mode.width, 
                        (mode.height // 1.65) - 1/12* mode.height, 
                        (mode.width // 2) + 1/4* mode.width,
                        (mode.height // 1.65) + 1/12* mode.height)
        helpX0, helpY0, helpX1, helpY1 = helpTab
        if (helpX0 <= x <= helpX1) and (helpY0 <= y <= helpY1):
            mode.helpFill = "red"
        else:
            mode.helpFill = "white"

    def timerFired(mode):
        mode.checkHover()

    def redrawAll(mode, canvas):
        mode.drawDesign(canvas)
        mode.drawTitle(canvas)
        mode.drawPlayTab(canvas)
        mode.drawHelpTab(canvas)
    
    def drawDesign(mode, canvas):
        #draw rectangle
        x0 = mode.width * 0.5/4
        x1 = mode.width * 3.5/4
        y0 = mode.height * 4.5/10
        y1 = mode.height
        canvas.create_rectangle(x0, y0, x1, y1, outline = "blue", width = 5)

        #draw arc
        x2 = mode.width * 0.5/4
        y2 = mode.height * 1/10
        x3 = mode.width * 3.5/4
        y3 = mode.height * 8/10
        canvas.create_arc(x2, y2, x3, y3, style = "chord", start = 0, extent = 180, width = 5, outline = "blue")


    def drawHelpTab(mode, canvas):
        helpTab = ((mode.width // 2) - 1/4* mode.width, 
                        (mode.height // 1.65) - 1/12* mode.height, 
                        (mode.width // 2) + 1/4* mode.width,
                        (mode.height // 1.65) + 1/12* mode.height)
        x0, y0, x1, y1 = helpTab
        canvas.create_rectangle(x0, y0, x1, y1, fill = mode.helpFill, width = 2)
        canvas.create_text(mode.width // 2, (y0 + y1) // 2, text = "Help",
                            font = "Arial 25 bold")

    def drawPlayTab(mode, canvas):
        playTab = ((mode.width // 2) - 1/4* mode.width, 
                        (mode.height // 2.5) - 1/12* mode.height, 
                        (mode.width // 2) + 1/4* mode.width,
                        (mode.height // 2.5) + 1/12* mode.height)
        x0, y0, x1, y1 = playTab
        canvas.create_rectangle(x0, y0, x1, y1, fill = mode.playFill, width = 2)
        canvas.create_text(mode.width // 2, (y0 + y1) // 2, text = "Play",
                            font = "Arial 25 bold")

    def drawTitle(mode, canvas):
        canvas.create_text(mode.width // 2, mode.height * 2/10, 
                            text = "NBA 112K", font = "Arial 35 bold")

class MyModalApp(ModalApp):
    def appStarted(app):
        app.menuMode = MenuMode()
        app.helpMode = HelpMode()
        app.setActiveMode(app.menuMode)

app = MyModalApp(width = 650, height = 550)