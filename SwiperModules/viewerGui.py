import os
import shutil
import tkinter as tk
import urllib.request

from PIL import ImageTk, Image
from webptools import webplib as webp


def download(link: str):
    if link[-3:] == "ebp":
        urllib.request.urlretrieve(link, "./temp.webp")
        webp.dwebp("temp.webp", "picture.png", "-o")
    else:
        urllib.request.urlretrieve(link, "./temp.jpg")
        im1 = Image.open("./temp.jpg")
        im1.save("picture.png")


def getLastFileId(fileName) -> int:
    try:
        fileNumber = len(os.listdir(fileName))
        return fileNumber
    except FileNotFoundError:
        os.mkdir(fileName)
        return 0


class Viewer:
    def __init__(self, picture_url_list: list):
        self.root = tk.Tk()
        self.linkList = picture_url_list
        self.sum = 0
        self.iter = 0
        self.lastNoFileindex = getLastFileId("no")
        self.lastYesFileindex = getLastFileId("yes")

    def picMove(self, doLikeIt):
        if doLikeIt:
            self.lastYesFileindex += 1
            shutil.move('picture.png', f'yes/{self.lastYesFileindex}.png')
        else:
            self.lastNoFileindex += 1
            shutil.move('picture.png', f'no/{self.lastNoFileindex}.png')

    # GUI stuff
    def getNextLink(self):
        if len(self.linkList) == 0:
            return ""
        link = self.linkList.pop(0)
        return link

    def setList(self, listOfUrls):
        self.linkList = listOfUrls
        self.sum = 0
        self.iter = 0

    def isPersonFaceless(self):
        if (len(self.linkList) == 1) & (self.linkList[0].find("unknown.jpg") != -1):  # wyrzyca ludzi bez mordy
            return True

    def pictureBrowser(self):
        if self.isPersonFaceless():
            return 0
        display = ""
        label = ""
        self.root.title('TinderSwiPy- Do You like her? (AI learn)')

        def update_pic():
            next_pic = self.getNextLink()
            if next_pic == "":
                self.root.quit()
            else:
                download(next_pic)
                nonlocal display
                nonlocal label
                display = ImageTk.PhotoImage(Image.open("./picture.png"))
                label = tk.Label(self.root, image=display)
                label.grid(row=0, column=0, columnspan=3)

        update_pic()

        def swipe(side):
            # side=0 swipeNo
            # side=1 swipeYes
            # side=2 swipeUseless (for example when picture presents dog.)
            self.iter += 1
            self.sum += side % 1.5
            if side <= 1:
                self.picMove(True if side > 0 else False)
            update_pic()

        # Buttons
        yes_button = tk.Button(self.root, text="Yes", padx=10, pady=5, fg="white", bg="#263D42",
                               command=lambda: swipe(1)).grid(
            row=1, column=2)
        no_button = tk.Button(self.root, text="Nope", padx=10, pady=5, fg="white", bg="#263D42",
                              command=lambda: swipe(0)).grid(
            row=1, column=0)
        useless_button = tk.Button(self.root, text="It's not a human", padx=10, pady=5, fg="white", bg="#263D42",
                                   command=lambda: swipe(2)).grid(row=1, column=1)
        # Keys input
        self.root.bind("<Down>", lambda e: swipe(2))
        self.root.bind("<Right>", lambda e: swipe(1))
        self.root.bind("<Left>", lambda e: swipe(0))
        self.root.mainloop()
        return self.sum / self.iter if self.iter != 0 else 0
