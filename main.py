import time
import tkinter
from tkinter import PhotoImage
from typing import Optional, Union, Tuple

import PIL.Image
import customtkinter
from tkinter import Label
from tkinter import Label
from PIL import ImageTk
from PIL import Image
from ntcore import NetworkTableInstance

inst = NetworkTableInstance.getDefault()
inst.startClient4("ClosestNode")
inst.startServer()
inst.setServer("127.0.0.1", NetworkTableInstance.kDefaultPort4)

number = 0
hasReset = False


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        image = PhotoImage(file="teamLogo.png")
        self.iconphoto(False, image)
        self.resizable(height=None, width=None)
        self.minsize(900, 100)
        self.maxsize(900, 100)
        self.title("ClosestNode")

        customtkinter.set_appearance_mode("dark")

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
    number = inst.getTable('SmartDashboard').getNumber("ClosestNode", -1)

    global hasReset
    if not number == -1:
        hasReset = False
        reset()
        nodes[number].configure(image=customtkinter.CTkImage(
                                                    dark_image=Image.open("yellow.png"),
                                                    size=(100, 100)), text_color="black")
    else:
        if not hasReset:
            reset()
            hasReset = True

    app.after(100, task)


def reset():
    for x in range(9):
        nodes[x].configure(image=customtkinter.CTkImage(
            dark_image=Image.open("gray-removebg-preview.png"),
            size=(100, 100)), text_color="white")


if __name__ == '__main__':
    app = App()
    app.after(100, task)
    app.mainloop()
