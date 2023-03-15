import tkinter
from tkinter import PhotoImage

import customtkinter

from PIL import Image
from ntcore import NetworkTableInstance

inst = NetworkTableInstance.getDefault()
inst.startClient4("ClosestNode")
inst.startServer()

table = inst.getTable("LimelightVals")
limelightTable = inst.getTable("limelight")

number = 0
hasReset = False

limelightValReset = False

tvPub = table.getDoubleTopic("tv").publish()
botPosePub = table.getDoubleArrayTopic("botpose").publish()


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        image = PhotoImage(file="teamLogo.png")
        self.iconphoto(False, image)
        self.resizable(height=None, width=None)
        self.minsize(900, 125)
        self.maxsize(900, 125)
        self.title("ClosestNode")

        customtkinter.set_appearance_mode("dark")

        global ipEntry
        ipEntry = customtkinter.CTkEntry(master=self, placeholder_text="Enter IP:")
        ipEntry.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        global connectingLabel
        connectingLabel = customtkinter.CTkLabel(master=self, text="Connecting...", font=("Exo", 20))
        connectingLabel.place(relx = 0, rely = 0.85, anchor = tkinter.W)


        global gamePieceArray
        gamePieceArray = []
        gamePieceArray.append(customtkinter.CTkLabel(self,
                                                image = customtkinter.CTkImage(
                                                    dark_image= Image.open("greySquare.PNG"),
                                                    size= (30,30)),
                                                anchor=customtkinter.E,
                                                text = ""))


        gamePieceArray.append(customtkinter.CTkLabel(self,
                                                image=customtkinter.CTkImage(
                                                    dark_image=Image.open("greySquare.PNG"),
                                                    size=(30, 30)),
                                                anchor=customtkinter.E,
                                                text=""))

        gamePieceArray[0].place(relx = 0.86 + 0.05, rely = 0.8)
        gamePieceArray[1].place(relx = 0.9 + 0.05, rely = 0.8)


        global nodes
        nodes = []
        for x in range(10):
            nodes.append(customtkinter.CTkLabel(self,
                                                image=customtkinter.CTkImage(
                                                    dark_image=Image.open("gray-removebg-preview.png"),
                                                    size=(100, 100)),
                                                text=x + 1,
                                                anchor=customtkinter.CENTER,
                                                font=("Exotica", 48),
                                                text_color="white"
                                                ))
            nodes[x].grid(row=0, column=x)

def task():
    if not inst.isConnected():
        global tvPub
        global botPosePub
        global limelightValReset
        limelightValReset = False
        setColor('None', 0)
        setColor('None', 1)
        reset()
        if len(ipEntry.get()) >= 9 and (
                ipEntry.get() == "127.0.0.1" or ("10." in ipEntry.get() and ".2" in ipEntry.get())):
            inst.setServer(ipEntry.get(), NetworkTableInstance.kDefaultPort4)
        connectingLabel.configure(text="Connecting...")
    else:
        if not limelightValReset:
            tvPub.close()
            botPosePub.close()
            botPosePub = table.getDoubleArrayTopic("botpose").publish()
            tvPub = table.getDoubleTopic("tv").publish()
            limelightValReset = True
        isRedAlliance = inst.getTable("FMSInfo").getBoolean("IsRedAlliance", False)
        connectingLabel.configure(text="Connected!")
        number = inst.getTable('SmartDashboard').getNumber("ClosestNode", -1)

        # print(inst.getTable('limelight').getNumber("tv", -1))
        sendLimeLightValues()

        firstGamePieceValue = inst.getTable('AdvantageKit/RealOutputs/ColorSensor').getString("GamePieceArray[0]", "")
        secondGamePieceValue = inst.getTable('AdvantageKit/RealOutputs/ColorSensor').getString("GamePieceArray[1]", "")

        # print(firstGamePieceValue)
        # print(secondGamePieceValue)

        setColor(firstGamePieceValue, 0)
        setColor(secondGamePieceValue, 1)

        # print(isRedAlliance)
        global hasReset
        if not number == -1:
            hasReset = False
            reset()
            if isRedAlliance:
                nodes[int(number)].configure(image=customtkinter.CTkImage(
                    dark_image=Image.open("yellow.png"),
                    size=(100, 100)), text_color="black")
            else:
                nodes[8-int(number)].configure(image=customtkinter.CTkImage(
                                                            dark_image=Image.open("yellow.png"),
                                                            size=(100, 100)), text_color="black")
        else:
            if not hasReset:
                reset()
                hasReset = True

    app.after(100, task)
def sendLimeLightValues():
    tvPub.set(float(inst.getTable('limelight').getNumber("tv", -1)))
    botPosePub.set(inst.getTable('limelight').getNumberArray("botpose", []))

def reset():
    for x in range(9):
        nodes[x].configure(image=customtkinter.CTkImage(
            dark_image=Image.open("gray-removebg-preview.png"),
            size=(100, 100)), text_color="white")

def setColor(color, position):
    if color == "Cube":
        gamePieceArray[position].configure(image = customtkinter.CTkImage(
            dark_image=Image.open("purpleSquare.PNG")))
    elif color == "Cone":
        gamePieceArray[position].configure(image=customtkinter.CTkImage(
            dark_image=Image.open("yellowSquare.PNG")))
    else:
       gamePieceArray[position].configure(image=customtkinter.CTkImage(
            dark_image=Image.open("greySquare.PNG")))


if __name__ == '__main__':
    app = App()
    app.after(100, task)
    app.mainloop()
