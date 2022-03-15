from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import json
import os
import random
import sys


# App constants
WIDTH = 1000
HEIGHT = 650


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Function for opening text files
def open_file(name, mode="r", data=None):
    file_path = resource_path(name)

    if mode == "r":
        with open(file_path, mode, encoding='utf-8') as f:
            data = json.load(f)
            return data

    elif mode == "w":
        with open(file_path, mode, encoding='utf-8') as f:
            json.dump(data, f)


# Main Class


class App():
    def __init__(self, master):
        self.master = master
        self.master.config(bg="light steel blue")
        self.master.geometry(f'{WIDTH}x{HEIGHT}+500+200')
        self.master.resizable(width=False, height=False)
        self.master.title('Name the Picture')

        self.master.bind('<Return>', self.check_answer)

        # Timer
        self.time = 11
        self.timer = False
        self.running = False
        self.clickk = False

        # Load data
        self.load_data = open_file(resource_path("nahosemenne.json"))

        # Variables and Costants
        self.mistake = 0
        self.score = 0

        self.start, self.nwstart = 0, 0
        self.end, self.nwend = len(self.load_data)-1, len(self.load_data)-1

        self.data = self.load_data[self.start:self.end+1]
        self.index = random.randint(0, self.end-self.start)

        # On start
        self.draw_screen()
        self.draw_time()
        self.draw_image(resource_path(self.data[self.index]["img"]))

    def check_answer(self, event=None):
        name = self.entry.get().lower()

        # Check answer and put another image
        if len(self.data) > 0:
            if name == self.data[self.index]["name"] and self.time > 0:

                # If asnwer is correct
                self.entry.delete(0, END)

                self.data.pop(self.index)
                self.end -= 1

                self.mistake = 0
                self.score += 1

                if self.end - self.start > 0:
                    self.index = random.randint(0, self.end - self.start)
                else:
                    self.index = 0

                self.image_label.destroy()

                if len(self.data) > 0:
                    self.draw_image(resource_path(
                        self.data[self.index]["img"]))

                self.alert("light green", "CORRECTLY")
                self.time = 11

            else:
                # If answer is incorrect
                if self.mistake < 2:
                    self.mistake += 1

                else:
                    # Put another image after 3 mistakes
                    self.entry.delete(0, END)
                    self.mistake = 0

                    if self.score >= 0.5:
                        self.score -= 0.5

                    old = self.index

                    if self.end - self.start > 0:
                        self.index = random.randint(0, self.end - self.start)
                    else:
                        self.index = 0

                    self.image_label.destroy()
                    self.draw_image(resource_path(
                        self.data[self.index]["img"]))

                    self.alert(
                        "red", f"""WRONG\n{self.data[old]['name']}""")

                    self.time = 11

    def draw_image(self, image):
        # Draw main image
        load_img = Image.open(image)
        load_img.thumbnail((680*1.5, 680*1.5))
        render = ImageTk.PhotoImage(load_img)
        self.image_label = Label(self.master, image=render)
        self.image_label.image = render
        self.image_label.place(x=-5, y=-255)

        Label(self.master, text=f"{self.score}", font=(
            "Sogue", 25), background="light steel blue").place(x=WIDTH / 2, y=HEIGHT-45)

    def draw_screen(self):

        # End Screen
        Label(self.master, text="The course is completely done",
              font=("Sogue", 45), bg="light steel blue").place(x=0, y=0, width=WIDTH, height=HEIGHT)

        Button(self.master, text="Restart",
               command=self.restart, font=("Helvetice", 15), height=1, width=10, relief=FLAT).place(x=440, y=400)

        # Input area
        self.entry = Entry(self.master, bd=0, width=26, font=("Sogue", 12))
        self.entry.place(x=200, y=563, width=480, height=40)
        self.entry.insert(0, "")

        # Check Button
        button = Button(self.master, text="Check",
                        command=self.check_answer, font=("Helvetice", 15), height=1, width=10)
        button.config(relief=FLAT)
        button.place(x=680, y=563)

        # Timer button
        self.photo = PhotoImage(file=resource_path("timer.gif"))
        b = Button(self.master, command=self.click,
                   justify=LEFT)
        b.config(image=self.photo, width="32", height="32", relief=FLAT)
        b.pack(side=LEFT)
        b.place(x=50, y=565)

        # Setting button
        self.photo1 = PhotoImage(file=resource_path("settings.gif"))
        b1 = Button(self.master, command=self.set_image_range,
                    justify=LEFT)
        b1.config(image=self.photo1, width="32", height="32", relief=FLAT)
        b1.pack(side=LEFT)
        b1.place(x=WIDTH-100, y=565)

    def alert(self, color, text, time=1500):
        # Show after 3 mistake or after correct answer
        self.running = False
        vis = Label(self.master, text=text, font=("Sogue", 45), bg=color)
        vis.place(x=0, y=0, width=WIDTH, height=HEIGHT)
        vis.after(time, lambda: (vis.destroy(), self.run()))

    def restart(self):
        # Restart test
        self.start = self.nwstart
        self.end = self.nwend
        self.time = 11

        self.score = 0

        self.clickk = False

        self.data = self.load_data[self.start:self.end+1]
        self.index = random.randint(0, self.end-self.start)
        self.mistake = 0

        self.draw_screen()
        self.draw_time()
        self.draw_image(resource_path(self.data[self.index]["img"]))

    def run(self):
        # Start timer
        if not self.running and self.clickk:
            self.running = True
            self.countdown()

    def countdown(self):
        # Countdown time every sec
        if self.running and len(self.data) > 0:
            self.time -= 1
            if self.time <= 0:
                self.mistake = 2
                self.check_answer()
            try:
                self.label.destroy()
            except AttributeError:
                pass

            self.draw_time()
            self.master.after(1000, self.countdown)

        elif len(self.data) <= 0:
            self.running = False
            self.label.destroy()

    def draw_time(self):
        # Draw time on screen if timer is running
        if self.running:
            self.label = Label(self.master, text=f"{self.time}",
                               font=("Helvetice", 20), bg="light steel blue", anchor=CENTER)
            self.label.place(x=95, y=565)

    def click(self):
        if not self.clickk:
            self.clickk = True
        else:
            self.clickk = False
            self.running = False
            self.time = 11
            self.label.destroy()

        self.run()

    def set_image_range(self):
        # Set up new window
        newWindow = Toplevel(self.master)

        newWindow.title("Settings")
        newWindow.geometry("400x200+800+400")
        newWindow.resizable(width=False, height=False)
        newWindow.grab_set()

        Label(newWindow,
              text="Set up your image range").pack()

        self.start_value = Scale(newWindow, from_=1, to=len(
            self.load_data), orient=HORIZONTAL, sliderrelief='flat', activebackground='#73B5FA')
        self.start_value.set(self.nwstart + 1)
        self.start_value.pack()

        self.end_value = Scale(newWindow, from_=1, to=len(
            self.load_data), orient=HORIZONTAL, sliderrelief='flat', activebackground='#73B5FA')
        self.end_value.set(self.nwend + 1)
        self.end_value.pack()

        Button(newWindow, text="Set",
               command=self.get_image_range, justify=LEFT).pack()

    def get_image_range(self):
        self.nwstart = self.start_value.get() - 1
        self.nwend = self.end_value.get() - 1
        if self.nwend < self.nwstart:
            self.nwend, self.nwstart = self.nwstart, self.nwend

        self.restart()


root = Tk()
app = App(root)
root.mainloop()
